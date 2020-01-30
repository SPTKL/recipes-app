from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from ast import literal_eval
from pathlib import Path
import dash
import dash_auth
import json
import requests
import os
import base64
import datetime
import io
import tempfile
from layout import layout

base_url=os.environ['BASE_URL']
external_stylesheets = ['https://codepen.io/sptkl/pen/gObvrKQ.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.layout = layout

@app.callback(Output('SchemaName', 'children'),
              [Input('SchemaNameRadio', 'value')])
def display_schema(value):
    schema_names = requests.get(f'{base_url}/recipes/schema_names').json()['result']
    schema_options = [{'label': i['schema_name'], 'value': i['schema_name']} for i in schema_names]
    if value == 'N': 
        return html.Div([
            html.H6('Schema Name'),
            dcc.Dropdown(
                id='schema',
                options=schema_options,
                value='test'
            ),
        ])
    else: 
        return html.Div([
            html.H6('Schema Name'),
            dcc.Input(
                    id='schema',
                    value='',
                    placeholder='enter new schema name here',
                    type='text',
                    style={'width': '100%'}
                )
        ])

@app.callback(Output('UpdateArea', 'children'),
              [Input('schema', 'value')],
              [State('SchemaNameRadio', 'value')])
def display_updates(schema, SchemaNameRadio):
    if SchemaNameRadio == 'N': 
        r = requests.get(f'{base_url}/recipes/api/{schema}')\
                        .json()['result'][0]
        last_update = r.get('last_update', '')
        record = r.get('config', {})
    else: 
        record = {}
        last_update = 'NA'
    return html.Div([
                html.H6(f'last updated: {last_update}'),
                html.H6('Version Name'),
                dcc.Input(
                    id='version_name',
                    value=record.get('version_name', ''),
                    type='text',
                    placeholder='e.g. 20v1',
                    style={'width': '100%'}
                ),
                html.H6('dstSRS'),
                dcc.Input(
                    id='dstSRS',
                    value=record.get('dstSRS', ''),
                    type='text',
                    placeholder='e.g. EPSG:4326',
                    style={'width': '100%'}
                ), 
                html.H6('srcSRS'),
                dcc.Input(
                    id='srcSRS',
                    value=record.get('srcSRS', ''),
                    type='text',
                    placeholder='e.g. EPSG:2263',
                    style={'width': '100%'}
                ),
                html.H6('Geometry Type'),
                dcc.Input(
                    id='geometryType',
                    value=record.get('geometryType', ''),
                    type='text',
                    placeholder='e.g. MULTIPOLYGON',
                    style={'width': '100%'}
                ),
                html.H6('Layer Creation Options'),
                dcc.Input(
                    id='layerCreationOptions',
                    value=str(record.get('layerCreationOptions', '')),
                    type='text',
                    placeholder='''e.g. ['OVERWRITE=YES', 'PRECISION=NO']''',
                    style={'width': '100%'}
                ),
                html.H6('Src Open Options'),
                dcc.Input(
                    id='srcOpenOptions',
                    value=str(record.get('srcOpenOptions', '')),
                    type='text',
                    placeholder='''e.g. ['AUTODETECT_TYPE=NO', 'EMPTY_STRING_AS_NULL=YES', 'GEOM_POSSIBLE_NAMES=the_geom']''',
                    style={'width': '100%'}
                ),
                html.H6('New Field Names'),
                dcc.Input(
                    id='newFieldNames',
                    value=str(record.get('newFieldNames', '')),
                    type='text',
                    placeholder='''e.g. ['BOROUGH', 'BLOCK', 'LOT', ...]''',
                    style={'width': '100%'}
                ),
                html.H6('metaInfo'),
                dcc.Input(
                    id='metaInfo',
                    value=record.get('metaInfo', ''),
                    type='text',
                    placeholder='e.g. from NYC Opendata',
                    style={'width': '100%'}
                ),
                html.H6('Uploading New Data?'),
                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': 'Yes', 'value': 'Y'},
                            {'label': 'No', 'value': 'N'}
                        ],
                        value='Y',
                        labelStyle={'display': 'inline-block'}, 
                        id='UploadNew'
                    ), 
                    dcc.RadioItems(
                        options=[
                            {'label': 'Public', 'value': 'public-read'},
                            {'label': 'Private', 'value': 'private'}
                        ],
                        value='public-read',
                        labelStyle={'display': 'inline-block'}, 
                        id='ACL'
                    )
                ]),
                html.Div([
                    html.H6('path'),
                    dcc.Input(
                        id='path',
                        value=record.get('path', ''),
                        type='text',
                        placeholder='e.g. https://raw.githubusercontent.com/file.csv',
                        style={'width': '100%'}
                    )
                ], id='PathArea'), 
                dcc.Upload(
                    id='UploadArea',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]))
            ])
            
@app.callback([Output('UploadArea', 'style'),
            Output('PathArea', 'style')],
            [Input('UploadNew', 'value')])
def path_or_upload(value): 
    upload_style = {'width': '100%',
                    'height': '100px',
                    'lineHeight': '100px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'display': 'none' if value=='N' else 'block'}

    path_style = {'display': 'none' if value=='Y' else 'block'}

    return upload_style, path_style

@app.callback(Output('UploadStatusArea', 'children'),
              [Input('UploadArea', 'contents')],
              [State('UploadArea', 'filename'),
               State('UploadArea', 'last_modified')])
def display_upload_status(contents, filename, last_modified):
    return html.Div([
        html.H5('Upload Complete 🙌🙌🙌'),
        html.H6(f'File Name: {filename}'),
        html.H6(f'Last Modified Date : {datetime.datetime.fromtimestamp(last_modified).strftime("%Y/%m/%d")}')
    ])

@app.callback(Output('UpdateMessageArea', 'style'),
                [Input('UpdateButton', 'n_clicks')])
def show_spinner(n_clicks): 
    if n_clicks and n_clicks>=1:
        return {'visibility': 'visible'}

@app.callback(Output('UpdateMessageArea', 'children'),
            [Input('UpdateButton', 'n_clicks')],
            [State('UploadArea', 'contents'),
            State('UploadArea', 'filename'),
            State('UploadArea', 'last_modified'),
            State('UploadNew', 'value'),
            State('ACL', 'value'),
            State('schema', 'value'),
            State('version_name', 'value'), 
            State('path', 'value'), 
            State('dstSRS', 'value'), 
            State('srcSRS', 'value'),
            State('geometryType', 'value'),
            State('metaInfo', 'value'),
            State('layerCreationOptions', 'value'),
            State('srcOpenOptions', 'value'),
            State('newFieldNames', 'value')])
def submit_update(n_clicks, contents, filename, 
                last_modified, upload, acl, schema, 
                version_name, path, dstSRS, srcSRS, 
                geometryType, metaInfo, layerCreationOptions, 
                srcOpenOptions, newFieldNames):
    if upload == 'Y':
        suffix = Path(filename).suffix
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        last_modified = datetime.datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d")
        version_name = '' if version_name.strip() == '' else version_name.strip()

        x = requests.post(f'{base_url}/upload',
            files = {'file': decoded},
            data = {'key': f'{last_modified}/{filename}', 'acl': acl})
        print(x)
        print(x.content)
        r = json.loads(x.content)
        if n_clicks and n_clicks>=1:
            if r['url'] != '': 
                config={
                    'schema_name': schema,
                    'version_name': '' if version_name==None else version_name,
                    'path': r['url'], 
                    'geometryType': geometryType,
                    'srcSRS': srcSRS,
                    'dstSRS': dstSRS,
                    'layerCreationOptions': literal_eval(layerCreationOptions),
                    'srcOpenOptions': literal_eval(srcOpenOptions),
                    'newFieldNames': literal_eval(newFieldNames)
                }
                r = requests.post(f'{base_url}/archive', data=json.dumps(config))
                response = json.loads(r.text)
                if response['status'] == 'success':
                    return html.H6(f'{schema} has been updated!')
                else:
                    return html.Div([
                        html.H6(f'something went wrong {schema} has been updated!'), 
                        html.H6(f'{str(response)}')
                    ])
    else:
        if n_clicks and n_clicks>=1:
            config={
                'schema_name': schema,
                'version_name': '' if version_name==None else version_name,
                'path': path, 
                'geometryType': geometryType,
                'srcSRS': srcSRS,
                'dstSRS': dstSRS,
                'layerCreationOptions': literal_eval(layerCreationOptions),
                'srcOpenOptions': literal_eval(srcOpenOptions),
                'newFieldNames': literal_eval(newFieldNames)
            }
            r = requests.post(f'{base_url}/archive', data=json.dumps(config))
            response = json.loads(r.text)
            if response['status'] == 'success':
                return html.H6(f'{schema} has been updated!')
            else:
                return html.Div([
                    html.H6(f'something went wrong {schema} has been updated!'), 
                    html.H6(f'{str(response)}')
                ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
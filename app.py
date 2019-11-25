import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from ast import literal_eval
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import numpy as np
import json
import os
from archiver import archiver

# all the datapreparation part will take place here
recipe_url = 'recipes.csv'
df = pd.read_csv(recipe_url)
df = df.replace(np.nan, '', regex=True)

schemas = df['schema_name'].to_list()
schema_options = [dict(label=i, value=i) for i in schemas]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('EDM data recipes yay!'),
    html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Create New', 'value': 'Y'},
                    {'label': 'Existing', 'value': 'N'}
                ],
                value='N',
                labelStyle={'display': 'inline-block'}, 
                id='SchemaNameRadio'
            ),

            html.Div(id='SchemaName'),

            html.Div(id='UpdateArea'),

            html.Button('Submit', id='UpdateButton'), 

            html.Div(id='UpdateMessageArea')

        ])
    ])

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )
    
@app.callback(Output('SchemaName', 'children'),
              [Input('SchemaNameRadio', 'value')])
def display_schema(value): 
    if value == 'N': 
        return html.Div([
            html.H4('Schema Name'),
            dcc.Dropdown(
                id='schema',
                options=schema_options,
                value='dep_wwtc'
            ),
        ])
    else: 
        return html.Div([
            html.H4('Schema Name'),
            dcc.Input(
                    id='schema',
                    placeholder='enter new schema name here',
                    type='text',
                    style={'width': '100%'}
                )
        ])

@app.callback(Output('UpdateArea', 'children'),
              [Input('schema', 'value')])
def display_updates(schema):
    try:
        record = df.loc[df.schema_name==schema].to_dict('records')[0]
    except: 
        record = {}
    return html.Div([
                html.H4('Version Name'),
                dcc.Input(
                    id='version_name',
                    value=record.get('version_name', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('dstSRS'),
                dcc.Input(
                    id='dstSRS',
                    value=record.get('dstSRS', ''),
                    type='text',
                    style={'width': '100%'}
                ), 
                html.H4('srcSRS'),
                dcc.Input(
                    id='srcSRS',
                    value=record.get('srcSRS', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('Geometry Type'),
                dcc.Input(
                    id='geometryType',
                    value=record.get('geometryType', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('Layer Creation Options'),
                dcc.Input(
                    id='layerCreationOptions',
                    value=record.get('layerCreationOptions', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('Src Open Options'),
                dcc.Input(
                    id='srcOpenOptions',
                    value=record.get('srcOpenOptions', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('New Field Names'),
                dcc.Input(
                    id='newFieldNames',
                    value=record.get('newFieldNames', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('metaInfo'),
                dcc.Input(
                    id='metaInfo',
                    value=record.get('metaInfo', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H5('Uploading New Data?'),
                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': 'Yes', 'value': 'Y'},
                            {'label': 'No', 'value': 'N'}
                        ],
                        value='N',
                        labelStyle={'display': 'inline-block'}, 
                        id='UploadNew'
                    )
                ]),
                html.Div([
                    html.H4('path'),
                    dcc.Input(
                        id='path',
                        value=record.get('path', ''),
                        type='text',
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

@app.callback(Output('UpdateMessageArea', 'children'),
            [Input('UpdateButton', 'n_clicks')],
            [State('UploadNew', 'value'),
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
def submit_update(n_clicks, upload, schema, version_name, 
                path, dstSRS, srcSRS, geometryType, 
                metaInfo, layerCreationOptions, 
                srcOpenOptions, newFieldNames):
    if n_clicks and n_clicks>=1:
        try: 
            archiver.archive_table(
                config={'schema_name': schema,
                    'version_name': '' if version_name==None else version_name,
                    'path': path, 
                    'geometryType': geometryType,
                    'srcSRS': srcSRS,
                    'dstSRS': dstSRS
                    })
            return html.H4(f'{schema} has been updated!')
        except Exception as e:
            return html.Div([
                html.H4(f'something went wrong {schema} has been updated!'), 
                html.H5(f'{str(e)}')
                ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8003)
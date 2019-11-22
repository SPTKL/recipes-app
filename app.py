import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# all the datapreparation part will take place here
recipe_url = 'recipes.csv'
df = pd.read_csv(recipe_url)
schemas = df['schema_name'].to_list()
schema_options = [dict(label=i, value=i) for i in schemas]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('EDM data recipes yay!'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Update Old Dataset', value='tab-1'),
        dcc.Tab(label='Create New Dataset', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Select Exisiting Dataset'), 

            # select a table to update: 
            dcc.Dropdown(
                id='SelectSchema',
                options=schema_options,
                value='dcp_pluto'
            ),
            html.Div(id='UpdateArea'), 
            html.Button('Submit', id='button'),
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

@app.callback(Output('UpdateArea', 'children'),
              [Input('SelectSchema', 'value')])
def display_content(schema):
    record = df.loc[df.schema_name==schema].to_dict('records')[0]
    return html.Div([
                html.H4('version_name'),
                dcc.Input(
                    id='version_name',
                    value=record.get('version_name', ''),
                    type='text',
                    style={'width': '100%'}
                ),
                html.H4('path'),
                dcc.Input(
                    id='path',
                    value=record.get('path', ''),
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
                html.H4('metaInfo'),
                dcc.Input(
                    id='metaInfo',
                    value=record.get('metaInfo', ''),
                    type='text',
                    style={'width': '100%'}
                )
            ])
if __name__ == '__main__':
    app.run_server(debug=True, port=8002)
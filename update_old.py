# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
# from sqlalchemy import create_engine
# import pandas as pd
# import numpy as np
# # all the datapreparation part will take place here
# recipe_url = 'recipes.csv'
# df = pd.read_csv(recipe_url)
# schemas = df['schema_name'].to_list()
# schema_options = [dict(label=i, value=i) for i in schemas]
# #
# UpdateOld = html.Div([
#             html.H3('Select Exisiting Dataset'), 

#             # select a table to update: 
#             dcc.Dropdown(
#                 id='SelectSchema',
#                 options=schema_options,
#                 value='dcp_pluto'
#             ), 
#             html.Div(id='UpdateArea')
#         ])

# @app.callback(Output('UpdateArea', 'children'),
#               [State('SelectSchema', 'dcp_pluto')])
# def display_content(schema):
#     record = df.loc[df.schema_name==schema].to_dict('records')[0]

#     return html.Div([
#                 html.H4('version_name'),
#                 dcc.Input(
#                     id='version_name',
#                     placeholder=record.get('version_name', ''),
#                     type='text',
#                     value=''
#                 ),
#                 html.H4('path'),
#                 dcc.Input(
#                     id='path',
#                     placeholder=record.get('path', ''),
#                     type='text',
#                     value=''
#                 ), 
#                 html.H4('dstSRS'),
#                 dcc.Input(
#                     id='dstSRS',
#                     placeholder=record.get('dstSRS', ''),
#                     type='text',
#                     value=''
#                 ), 
#                 html.H4('srcSRS'),
#                 dcc.Input(
#                     id='srcSRS',
#                     placeholder=record.get('srcSRS', ''),
#                     type='text',
#                     value=''
#                 )
#             ])

import dash_html_components as html
import dash_core_components as dcc

header = html.Header([
    html.Div([
        html.Div([
                html.Div([
                    html.Img(src='https://raw.githubusercontent.com/NYCPlanning/dcp-logo/master/dcp_logo_772.png',
                            alt="NYC Planning",
                            style={'max-height': '4.5rem'},
                            className='header-logo medium-margin-right medium-margin-bottom')
                ], className='cell medium-shrink'),
                html.Div([
                    html.Div([
                        html.H1(children='EDM Data Recipes  🍣🍥🍙🍜🍲🍩', className='no-margin'),
                        html.P(children='EDM - Data Engineering', className='medium-margin-bottom')
                    ], id='title', className='no-margin')
                ], className='cell medium-auto'), 
                html.P([
                    html.A([
                        html.Img(src='/assets/GitHub-Mark-32px.png',
                            className='large-margin-top')
                    ], href='https://github.com/NYCPlanning/recipes')
                ],className='cell medium-shrink no-margin show-for-medium')
            ], className='grid-x text-center medium-text-left align-middle')
    ], className='grid-container')
], className='xlarge-padding-top large-padding-bottom bg-white-smoke')

body = html.Div([
    html.Div([
        html.Div([
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
                html.Div(id='UploadStatusArea'), 
                html.Button('Submit', id='UpdateButton', className='button expanded'),
                html.Div(
                    dcc.Loading(
                        id="UpdateMessageArea", 
                        type="circle",
                        style={'visibility': 'hidden'}
                        )
                    )
            ],id='control', className='sticky large-padding-top large-padding-bottom is-anchored is-at-top')
        ], className='medium-6 large-5 cell medium-order-1 sticky-container'), 
        html.Div([
           dcc.Markdown('''
                ### Instructions:
                #### Updating an exisiting table: 
                1. select the __schema name__ (table name) you are looking for, note the dropdown supports text search. 
                2. enter a __version name__. For pluto, DCP published shapfiles, use vintage, e.g. `20A`, `20B`, `20v2` and etc
                3. Specify __spatial reference__, e.g. `EPSG:4326`, `EPSG:2263`
                4. Specify __geometry type__, one of `NONE`, `GEOMETRY`, `POINT`, `LINESTRING`, `POLYGON`, `GEOMETRYCOLLECTION`, 
                `MULTIPOINT`, `MULTIPOLYGON`, `MULTILINESTRING`, `CIRCULARSTRING`, `COMPOUNDCURVE`, `CURVEPOLYGON`, `MULTICURVE`, and `MULTISURFACE`
                5. Specify __layer creation options__, e.g. `['OVERWRITE=YES', 'PRECISION=NO']`
                6. __SRC open options__, e.g. `['AUTODETECT_TYPE=NO', 'EMPTY_STRING_AS_NULL=YES', 'GEOM_POSSIBLE_NAMES=the_geom', 'X_POSSIBLE_NAMES=longitude,Longitude,Lon,lon,x', 'Y_POSSIBLE_NAMES=latitude,Latitude,Lat,lat,y']`
                7. Only fill in __new field names__ if we have a new list of columns names, make sure the order matches
                8. __Metainfo__ is for a brief description about the dataset, e.g. "data comes from opendata"
                9. Choose if you are loading data from a known url or upload new file. 

                #### Create new table: 
                1. choose a schema name that hasn't been used before.
                2. fill in the corresponding values according the above mentioned.
                ''')
        ], id='instructions', className='medium-6 large-7 cell medium-order-2 large-padding-top large-padding-bottom')
    ], className='grid-x grid-margin-x')
    ], className='grid-container', id='main-content')

layout = html.Div([
    header,
    body
])
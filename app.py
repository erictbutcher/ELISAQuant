import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import io
import base64
import helpers

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server

app.title = 'ELISAQuant'

app.layout = html.Div([
    #header
    html.Div([
        html.H1("ELISAQuant:", className = 'header-item'),
        html.H4("An app to easily and reproducibly quantify analyte concentration", className = 'header-item')
    ], id = 'header'),
    #body
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader("Upload Data"),
                dbc.CardBody([
                    html.Br(),
                    #data needed to process the data
                    html.Div([
                        dbc.Label("Choose Template", size = 'lg', style = {'width':'50%'}),
                        dbc.Button(html.Span([html.Img(src=app.get_asset_url('info.png'), style={'height':'100%', 'width':'100%'})]), color = 'link', id = 'temp-info-button', className = 'info-button'),
                        dbc.Modal([
                            dbc.ModalBody([
                                html.P("Please use one of the following two templates for your plate:"),
                                html.P("Option 1:"),
                                html.Img(src = app.get_asset_url('option_1.png'), style = {'width': '100%', 'height': '100%'}),
                                html.Br(),
                                html.Br(),
                                html.P("Option 2:"),
                                html.Img(src = app.get_asset_url('option_2.png'), style = {'width': '100%', 'height': '100%'})
                            ])
                        ], id = 'template-info')
                    ], className = 'whole-column'),
                    dbc.RadioItems(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                        ],
                        value=1,
                        id="template-input"),
                    html.Br(),
                    html.Div([
                        dbc.Label("Concentration for Standard Wells", size = 'lg', style = {'width':'85%'}),
                        dbc.Button(html.Span([html.Img(src=app.get_asset_url('info.png'), style={'height':'100%', 'width':'100%'})]), color = 'link', id = 'standards-info-button', className = 'info-button'),
                        dbc.Modal([
                            dbc.ModalBody("""
                                Enter the known analyte concentration of the standards in the
                                corresponding well of the plate. A standard curve using
                                a 5-parameter logistic regression will be fit according to
                                the known standards analyte concentration and the optical
                                density measured in the plate.""")
                        ], id = 'standards-info')
                    ], className = 'whole-column'),
                    html.Div([
                        dbc.Label('Standard 1', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard1')
                    ]),
                    html.Div([
                        dbc.Label('Standard 2', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard2')
                    ]),
                    html.Div([
                        dbc.Label('Standard 3', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard3')
                    ]),
                    html.Div([
                        dbc.Label('Standard 4', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard4')
                    ]),
                    html.Div([
                        dbc.Label('Standard 5', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard5')
                    ]),
                    html.Div([
                        dbc.Label('Standard 6', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard6')
                    ]),
                    html.Div([
                        dbc.Label('Standard 7', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard7')
                    ]),
                    html.Div([
                        dbc.Label('Standard 8', size = 'sm', style = {'width':'25%', 'display':'inline'}),
                        dbc.Input(type="number", style = {'width':'50%', 'display':'inline', 'margin':'5px'}, id = 'standard8')
                    ]),
                    html.Br(),
                    dcc.Upload(dbc.Button('Upload File'),id='upload-data'),
                    html.Br(),
                    dbc.Button('Perform Analysis', block = True, id = 'run-elisaquant')
                ])
            ])
        ], className = 'one-third-col'),
        html.Div([
            dbc.Card([
                dbc.CardHeader("About"),
                dbc.CardBody([
                    dcc.Markdown('''
                        An ELISA (enzyme-linked immunosorbent assay) is a plate-based
                        assay used to detect the presence and quantification of an
                        analyte.

                        In the final stages of the assay’s procedure an optical change
                        will occur in the liquid within the wells of the plate. The
                        quantification of the analyte is based on detection of intensity
                        of transmitted light by spectrophotometry, which involves
                        quantitation of transmission of some specific wavelength of
                        light through the liquid. The unit of measurement collected
                        is optical density. optical density is not a relevant unit of
                        measurement, but the optical density can be converted to something
                        more relevant from the known concentration of the assay standards.

                        ...

                    ''')
                ])
            ]),
            html.Br(),
            dbc.Card([
                dbc.CardHeader("Analysis"),
                dbc.CardBody([
                    html.Div(id='output-data-upload')
                ])
            ], style = {'text-align':'center'})
        ], className = 'two-thirds-col')
    ], id = 'content-container'),
    #footer
    html.Div([
        html.P("For more information and documentation, please visit this projects", className = 'footer-item'),
        dcc.Link("GitHub repo", href="https://www.google.com", className = 'footer-item')
    ], id = 'footer')
])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
              Input('template-input','value'),
              Input('standard1','value'),
              Input('standard2','value'),
              Input('standard3','value'),
              Input('standard4','value'),
              Input('standard5','value'),
              Input('standard6','value'),
              Input('standard7','value'),
              Input('standard8','value'),
              Input('run-elisaquant','n_clicks')])
def update_output(data,template, standard1, standard2, standard3, standard4,
    standard5, standard6, standard7, standard8, n_clicks):
    """
    """
    try:
        #data processing
        standards = [standard1, standard2, standard3,standard4, standard5, standard6, standard7, standard8]
        data_type, data_string = data.split(',')
        decoded = base64.b64decode(data_string)
        if 'csv' in data_type:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            children = [html.P("Data Uploaded")]
        elif 'octet-stream' in data_type:
            df = pd.read_excel(io.BytesIO(decoded))
            children = [html.P("Data Uploaded")]
        else:
            children = [html.P("This file type is not supported. Please use a .csv or .xls file")]
        #import pdb; pdb.set_trace()
    except:
        children = [html.P("Upload data for analysis")]
    #data analysis
    if n_clicks is not None:
        try:
            children = helpers.elisaquant(df,standards,template)
        except:
            children = [html.P("An error occured during analysis. Please review your data and ensure it was entered properly.")]
    return children

@app.callback(Output('template-info', 'is_open'),
              [Input('temp-info-button', 'n_clicks')],
              [State('template-info', 'is_open')])
def temp_info_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(Output('standards-info', 'is_open'),
              [Input('standards-info-button', 'n_clicks')],
              [State('standards-info', 'is_open')])
def standards_info_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == '__main__':
    application.run(debug=True, port=8080)

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_extensions import Download
import dash_table as dt
import pandas as pd
import numpy as np
import scipy.optimize as opt
import plotly.graph_objects as go

def logistic5(x, A, B, C, D, E):
    """5PL logistic equation
    A = Minimum asymptote. In a bioassay where you have a standard curve, this
        can be thought of as the response value at 0 standard concentration.
    B = Hill's slope. The Hill's slope refers to the steepness of the curve. It
        could either be positive or negative.
    C = Inflection point. The inflection point is defined as the point on the
        curve where the curvature changes direction or signs. C is the concentration
        of analyte where y=(D-A)/2.
    D = Maximum asymptote. In an bioassay where you have a standard curve, this
        can be thought of as the response value for infinite standard concentration.
    E = Asymmetry factor. When E=1 we have a symmetrical curve around inflection
        point and so we have a four-parameters logistic equation.
    """
    return D + ((A-D)/(np.power((1 + np.power((x / C), B)), E)))

def elisaquant(data, y, template):
    """
    """
    #Average the standards OD
    standards_x = data.loc[:, 0:1].mean(axis=1)
    #Avcerage the replicate samples
    if template == 1:
        samples_x = []
        for i in [3,5,7,9,11]:
            samples_x = np.concatenate([samples_x,data.loc[:, i:i+1].mean(axis=1).values])
    else:
        samples_x = []
        for i in range(2, 12):
            samples_x = np.concatenate([samples_x,[data[i].iloc[j:j+2,].values.mean() for j in [0,2,4,6]]])
        import pdb; pdb.set_trace()


    params, params_covariance = opt.curve_fit(logistic5, standards_x, y)
    #evaluation
    preds = pd.DataFrame({'Predictions':logistic5(samples_x, *params)})
    preds = preds.reset_index()
    preds = preds.rename(columns={'index':'Samples'})
    preds['Samples'] += 1
    #provide ability to download preds
    fig = go.Figure()
    fig.add_trace(go.Scatter(name = 'Standards', x = standards_x.values, y = y, mode='markers'))
    fig.add_trace(go.Scatter(name = 'Samples', x = samples_x, y = preds['Predictions'], mode='markers'))
    fig.update_layout(template='plotly_white', title='5-Parameter Logistic Regression Fit and Predictions')
    #fig.add_trace(go.Scatter(name = 'Curve'))
    children = [html.Div([
        dcc.Graph(figure = fig),
        html.Br(),
        html.Div([
            dbc.Label("Sample Predictions", style = {'margin-right':'5px'}),
            dbc.Button("Download csv", id="btn"), Download(id="download")
        ], style = {'display':'inline-block'}),
        dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in preds.columns],
            data=preds.to_dict('records'),
            style_table = {'overflowY': 'scroll', 'height':'500px'},
            style_cell={'textAlign': 'center'},
            style_cell_conditional=[
                {'if': {'column_id': 'Samples'},'width': '33%'},
                {'if': {'column_id': 'Predictions'},'width': '66%'}])
    ], style = {'height':'750px', 'overflow':'scroll'})]
    return children, preds


import dash
from dash import Dash, dcc, html, Input, State, Output, callback
import plotly.express as px
from data import *
import util

dash.register_page(__name__, path='/')


get_sbd = html.Div(style={'text-align': 'center', 'margin': '20px'},children = 
                [dcc.Input(id = 'id_input', placeholder= 'Nhập số báo danh của bạn', type='text'), 
                html.Button(id='submit-button', type='submit', children='Submit')]
)
user_sbd = html.Div(style={'textAlign': 'center'})

@callback(
        Output(user_sbd, component_property='children'),
        Input('submit-button', 'n_clicks'),
        State('id_input', 'value')
)
def sbd_callback(submitted, input_val):
    if submitted:
        if not input_val:
            return ''
        try:
            if len(input_val) != 8: raise ValueError # So bao danh hop le dai 8 ki tu
            if int(input_val):
                return dcc.Location(id = 'redirect', pathname=f'analytics\{input_val}')
        except ValueError:
            return f'Thay vì nhập {input_val}, xin hãy nhập một số báo danh hợp lệ.'

def layout(**custom):
    custom = util.remove_redundant_queries(custom)
    # Buttons to create custom combinations of subjects
    ## Combination container
    sj_container = html.Div(id='sj_container', children=[])
    
    ## Add a subject to the combination
    add_button = html.Button('Add', id='add-subject')
    ## Press this button to submit the custom combination
    submit = html.Button('Submit', id='submit-combination')
    res_submit = html.Div(id='res-submit')
    
    # Provide a custom graph if query string is provided
    if custom:
        all_graphs = util.create_graphs()
        all_graphs.insert(0, util.custom_combi(custom))
    else:
        all_graphs = util.create_graphs()
    return html.Div(
        children=([get_sbd, user_sbd,
        sj_container,
        add_button,
        submit,
        res_submit,
        ]
     + all_graphs))
import dash
from dash import Dash, dcc, html, Input, State, Output, callback
import plotly.express as px
from data import *
import util

dash.register_page(__name__, path='/', title='Dashboard')


get_sbd = html.Div(children = 
                [dcc.Input(id = 'id_input', placeholder= 'Nhập số báo danh của bạn', type='text'), 
                html.Button(id='submit-button', type='submit', children='Gửi')]
)
user_sbd = html.Div(id = 'user-sbd')

def layout(**custom):
    custom = util.remove_redundant_queries(custom)
    # Buttons to create custom combinations of subjects
    ## Combination container
    sj_container = html.Div(id='sj_container', children=[])
    
    ## Add a subject to the combination
    add_button = html.Button('Thêm môn học', id='add-subject')
    ## Press this button to submit the custom combination
    submit = html.Button('Gửi', id='submit-combination')
    res_submit = html.Div(id='res-submit')
    
    # Provide a custom graph if query string is provided
    if custom:
        all_graphs = util.create_graphs()
        all_graphs.insert(0, util.custom_combi(custom))
    else:
        all_graphs = util.create_graphs()
    return html.Div(
        children=([get_sbd,
            user_sbd,
            sj_container,
            add_button,
            submit,
            res_submit,
            ]
            + all_graphs))
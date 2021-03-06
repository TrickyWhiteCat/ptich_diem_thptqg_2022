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
    
    all_graphs = []
    for idx, val in enumerate(subjects):
        if val == 'Văn':
            all_graphs+=[util.create_graph(mon = val, graph_type='line'),  util.choropleth_w_slider(to_hop=val, id_obj=idx)]
        else:
            all_graphs+=[util.create_graph(mon = val),  util.choropleth_w_slider(to_hop=val, id_obj=idx)]
    
    # Provide a custom graph if query string is provided
    if custom:
        all_graphs= [util.custom_combi(custom), util.choropleth_w_slider(to_hop=custom, id_obj=idx+1)]
    return html.Div(
        children=([get_sbd,
            user_sbd,
            sj_container,
            add_button,
            submit,
            res_submit,
            ]
            + all_graphs))
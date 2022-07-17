import dash
from dash import Dash, dcc, html, Input, Output, State, callback, ALL
import util
from data import *
from dash.exceptions import PreventUpdate
import plotly.express as px

from util.func import bang_diem
dash.register_page(__name__, path_template="/analytics/<sbd>")


def layout(sbd=0, **custom):
    if sbd:
        custom = util.remove_redundant_queries(custom)
    
            # Create graphs for every subjects
        all_graphs = util.create_graphs(sbd)
            # Buttons to create custom combinations of subjects
    
            ## Combination container
        sj_container = html.Div(id='sj_container', children=[])
    
            
            ## Add a subject to the combination
        add_button = html.Button('Add', id='add-subject')
            ## Press this button to submit the custom combination
        submit = html.Button('Submit', id='submit-combination')
        res_submit = html.Div(id='res-submit')
            
        bang_diem(sbd)
    
            # Provide a custom graph if query string is provided
        if custom:
            all_graphs.insert(0, util.custom_combi(custom, sbd))
    
        return html.Div(
                        children = [
                            sj_container,
                            add_button, submit,
                            res_submit,
                            html.H4(children = f'Số báo danh: {sbd}', style={'text-align': 'center'}),
                            util.bang_diem(sbd),
                                    ] + all_graphs
            )
import dash
from dash import html
import util
from data import *

dash.register_page(__name__, path='/choro', title='So sánh điểm của các tỉnh')

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

    if custom:
        graph = util.choropleth_w_slider(to_hop=custom, id_obj=17)
    else:
        graph = html.Div()

    return html.Div(
            children = [
                sj_container,
                add_button,
                submit,
                res_submit,
                graph, # Just a random number..
            ])
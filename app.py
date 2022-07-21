from dash import Dash, html, dcc
import dash
import dash
from dash import Dash, dcc, html, Input, Output, State, callback, ALL, MATCH
from data import *
from dash.exceptions import PreventUpdate
from numpy import seterr

import json

import util


@callback(
    Output(component_id='sj_container', component_property= 'children'),
    Input(component_id='add-subject', component_property='n_clicks'),
    State(component_id='sj_container', component_property= 'children')
            )
def add_subject(clicks, children):
    ### A div containing a drop down list of subjects and the subjects' multiplier
    if not clicks:
        raise PreventUpdate
    subj = html.Div(
                id= f'subject-{clicks}',
                className='per-subject-container',
                children=
                    [dcc.Dropdown(dict(zip(subjects_lower, subjects)),
                        id = {'type': 'subject', 'index': clicks}, 
                        placeholder='Chọn môn',
                        className = 'subject-selector'),
                    dcc.Input(placeholder='Hệ số', className='multi', id={'type':'multi', 'index': 'click'})])
    children.append(subj)
            
    return children

@callback(
    Output(component_id='res-submit', component_property='children'),
    Input(component_id='submit-combination', component_property='n_clicks'),
    [
    State({'type':'subject', 'index': ALL}, 'value'),
    State({'type':'multi', 'index': ALL}, 'value')
    ]
    )
def submit_combination(click, subjects, multis):
    if not click:
        raise PreventUpdate
    combination = {}
    for item in zip(subjects, multis):
        if not (item[0] and item[1]):
            continue # Skip empty field
        try:
            if int(item[1]) != float(item[1]):
                raise ValueError
        except ValueError:
            return 'Hãy nhập hệ số là số nguyên'
        combination[item[0]] = int(item[1])
    if combination: # User may create a bunch of fields but fill in none of them. Only redirect when something valid was provided
        query_str = '&'.join([f"{val.replace(' ', '%20')}={combination[val]}" for val in combination.keys()])
        return dcc.Location(id = 'redirect-query', pathname='/', search=f'?{query_str}')

@callback(
    Output(component_id= {'type':'choro-w-slider', 'index':MATCH, 'subject': ALL}, component_property='children'),
    [Input(component_id={'type': 'slider-input', 'index':MATCH}, component_property='value'),
    Input(component_id={'type': 'region', 'index': MATCH}, component_property='value'),
    Input(component_id={'type': 'percent_sum', 'index':MATCH}, component_property='value')],
    [State(component_id= {'type':'choro-w-slider', 'index':MATCH, 'subject': ALL}, component_property='id'),
    State(component_id= {'type':'choro-w-slider', 'index':MATCH, 'subject': ALL}, component_property='children'),]
)
def set_level(input_value, region, percent, id_obj, children):
    id_obj = id_obj[0] # id_obj's type was "list"
    if id_obj['subject'] and region:
        try:
            mon = json.loads(id_obj['subject'])
        except json.decoder.JSONDecodeError:
            mon = id_obj['subject']
        children[0][2] = util.choropleth_map(mon = mon,
                                    muc_diem = input_value,
                                    percent = percent,
                                    region = region,
                                    idx = id_obj['index'])
    return children


@callback(
    Output(component_id={'type': 'slider', 'index':MATCH}, component_property= "value"),
    Output(component_id={'type': 'slider-input', 'index':MATCH}, component_property= "value"),
    Input(component_id={'type': 'slider', 'index':MATCH}, component_property= "value"),
    Input(component_id={'type': 'slider-input', 'index':MATCH}, component_property= "value"),
)
def match_input_slider(slider_value, input_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    value = input_value if 'slider-input' in trigger_id else slider_value
    return value, value

@callback(
        Output('user-sbd', component_property='children'),
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




es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, use_pages=True, pages_folder=r"pages", external_stylesheets=es)
app.title = 'Dashboard'
server=app.server
app.config.suppress_callback_exceptions=True
app.layout = html.Div([
	html.H1(id = 'header',children = ['Phân tích điểm thi THPT Quốc Gia 2022'], style={'text-align': 'center'}),
	dash.page_container
    ]
    )

if __name__ == '__main__':
    seterr(invalid='ignore')
    app.run_server(debug=False)

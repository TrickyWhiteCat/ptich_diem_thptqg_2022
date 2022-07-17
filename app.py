from dash import Dash, html, dcc
import dash
import dash
from dash import Dash, dcc, html, Input, Output, State, callback, ALL
from data import *
from dash.exceptions import PreventUpdate


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
        if not (item[0] and item[1]): continue # Skip empty field
        try:
            if int(item[1]) != float(item[1]):
                raise ValueError
        except ValueError:
            return 'Hãy nhập hệ số là số nguyên'
        combination[item[0]] = int(item[1])
    if combination: # User may create a bunch of fields but fill in none of them. Only redirect when something valid was provided
        query_str = '&'.join([f"{val.replace(' ', '%20')}={combination[val]}" for val in combination.keys()])
        return dcc.Location(id = 'redirect-query', pathname='/', search=f'?{query_str}')




es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, use_pages=True, pages_folder=r"pages", external_stylesheets=es)
server=app.server
app.config.suppress_callback_exceptions=True
app.layout = html.Div([
	html.H1(id = 'header',children = ['Phân tích điểm thi THPT Quốc Gia 2022'], style={'text-align': 'center'}),
	dash.page_container
    ]
    )

if __name__ == '__main__':
	app.run_server(debug=True)
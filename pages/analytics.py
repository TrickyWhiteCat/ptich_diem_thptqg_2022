import dash
from dash import Dash, dcc, html, Input, Output, State, callback, ALL
import util
from data import *
from dash.exceptions import PreventUpdate
import plotly.express as px
dash.register_page(__name__, path_template="/analytics/<sbd>")


def layout(sbd=0, **custom):
    if sbd:
        d = util.tra_diem(data, diem, sbd)

        # Create graphs for every subjects
        all_graphs = []
        personal_scores = diem[d.index] # Remove NaN scores

        for col in personal_scores.columns:
            data_to_plot = personal_scores[col].value_counts().sort_index()
            fig = px.line(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {col}', template="ggplot2")
            fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')

            info = html.Div(className='info', children = 
                        [html.H6(f'Điểm của bạn: {d[col]:.2f}'),
                        html.H6(f'''Điểm của bạn cao hơn {util.percentile(data=diem[col], value = d[col])} các thí sinh khác!
                         Chỉ có {util.higher(data=diem[col], value = d[col])} thí sinh có điểm cao hơn bạn!'''),
                        ])

            all_graphs.append(
                html.Div(className = 'fig_container' ,children=[
                    dcc.Graph(figure=fig, className='graph'),
                    info,
                    ]))

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
            all_graphs.insert(0, util.custom_combi(custom, sbd))

        return html.Div(
                        children = [
                            sj_container,
                            add_button, submit,
                            res_submit,
                            html.H4(children = f'Số báo danh: {sbd}', style={'text-align': 'center'}),
                            html.Table(
                                children=[
                                    html.Tr(className='subjects', children=
                                        [html.Th(className = 'subject', style={'text-align': 'center', 'border': '1px solid black'}, children = subject) for subject in d.index]),
                                    html.Tr(className = 'scores', children=
                                        [html.Td(className = 'score', style ={'text-align': 'center', 'border': '1px solid black'}, children = score) for score in d.values])
                                        ])
                                    ] + all_graphs
            )
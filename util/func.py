import pandas as pd
import numpy as np
from data import *
from dash.exceptions import PreventUpdate
import plotly.express as px
from dash import html, dcc


def tra_diem(data, diem, sbd: str):
    return diem.loc[data['SBD'] == int(sbd)].iloc[0].dropna()

def percentile(data: pd.DataFrame, value):
    'Return the percent of value that is SMALLER than given value'
    temp = data[data < value].count() / data.count()
    return f'{temp:.2%}'

def percentile_all_subjects(data: pd.DataFrame, diem, id: str):
    score = tra_diem(data, diem,id)
    for subject in score.index:
        if np.isnan(score[subject]): continue
        return f'Môn {subject}: {percentile(diem[subject], score[subject])}'

def higher(data: pd.DataFrame, value):
    'Return the percent of value that is SMALLER than given value'
    temp = data[data >= value].count()
    return f'{temp}'

def custom_combi(valid: dict, sbd = None):
    '''Return a graph of a custom combination of subjects
    Param:
    custom: a dictionary containing subjects and their multipliers
    sbd
    '''
    custom_data = sum([(diem[subjects[subjects_lower.index(val)]] * valid[val]) for val in valid.keys()])
    data_to_plot = custom_data.value_counts().sort_index()
    title = ", ".join([f'{subjects[subjects_lower.index(val)]} (hệ số {valid[val]})' for val in valid.keys()])
    if "van" in valid.keys():
        fig = px.line(x = data_to_plot.index.sort_values(), y = data_to_plot, template="ggplot2", title=(f'Điểm thi môn {title}'))
    else:
        fig = px.bar(x = data_to_plot.index.sort_values(), y = data_to_plot, template="ggplot2", title=(f'Điểm thi môn {title}'))
    fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')
    if sbd:
        d = tra_diem(data, diem, sbd)
        custom_d = sum([(d[subjects[subjects_lower.index(val)]] * valid[val]) for val in valid.keys()])

        info = html.Div(className='info', children = 
                    [html.H6(f'Điểm của bạn: {custom_d:.2f}'),
                    html.H6(f'''Điểm của bạn cao hơn {percentile(data=custom_data, value = custom_d)} các thí sinh khác!
                     Chỉ có {higher(data=custom_data, value = custom_d)} thí sinh có điểm cao hơn hoặc bằng bạn!'''),
                    ])
    else:
        info = html.Div(className='info', children = 
                [html.H6(f'Điểm trung bình: {custom_data.mean():.2f}'),
                html.H6(f'Số điểm nhiều thí sinh đạt được nhất: {custom_data.mode().iloc[0]}'),
                html.H6(f'Độ lệch chuẩn: {custom_data.std():.2f}'),
                ])

    return html.Div(
            className = 'fig_container',
            children=[
                dcc.Graph(figure=fig, className='graph'),
                info,
                ])

def remove_redundant_queries(query_str):
    valid = {}
    for val in query_str.keys():
        if val in subjects_lower:
            try:
                valid[val] = int(query_str[val])
            except ValueError:
                pass
    return valid

def create_graphs(sbd = 0):
    if sbd:
        d = tra_diem(data, diem, sbd)
        personal_sj = diem[d.index] # Remove NaN scores

    # Create graphs for every subjects
    all_graphs = []
    if sbd:
        for col in personal_sj.columns:
            if col == "Văn":
                data_to_plot = personal_sj[col].value_counts().sort_index()
                fig = px.line(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {col}', template="ggplot2")
                fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')
            else:
                data_to_plot = personal_sj[col].value_counts().sort_index()
                fig = px.bar(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {col}', template="ggplot2")
                fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')
            info = html.Div(className='info', children = 
                    [html.H6(f'Điểm của bạn: {d[col]:.2f}'),
                    html.H6(f'''Điểm của bạn cao hơn {percentile(data=diem[col], value = d[col])} các thí sinh khác! Chỉ có {higher(data=diem[col], value = d[col])} thí sinh có điểm cao hơn bạn!'''),
                    ])
            all_graphs.append(
                html.Div(className = 'fig_container' ,children=[
                    dcc.Graph(figure=fig, className='graph'),
                    info,
                    ]))
    else:
        for col in diem.columns:
            if col == "Văn":
                data_to_plot = diem[col].value_counts().sort_index()
                fig = px.line(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {col}', template="ggplot2")
                fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')
            else:
                data_to_plot = diem[col].value_counts().sort_index()
                fig = px.bar(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {col}', template="ggplot2")
                fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')

            info = html.Div(className='info', children = 
                        [html.H6(f'Điểm trung bình: {diem[col].mean():.2f}'),
                        html.H6(f'Số điểm nhiều thí sinh đạt được nhất: {diem[col].mode().iloc[0]}'),
                        html.H6(f'Độ lệch chuẩn: {diem[col].std():.2f}'),
                        ])

            all_graphs.append(
                html.Div(className = 'fig_container' ,children=[
                    dcc.Graph(figure=fig, className='graph'),
                    info,
                    ]))

    return all_graphs

def bang_diem(sbd):
    d = tra_diem(data, diem, sbd)
    return html.Table(
        children=[
            html.Tr(className='subjects', children=
                [html.Th(className = 'subject', style={'text-align': 'center', 'border': '1px solid black'}, children = subject) for subject in d.index]),
            html.Tr(className = 'scores', children=
                [html.Td(className = 'score', style ={'text-align': 'center', 'border': '1px solid black'}, children = score) for score in d.values])
                ])


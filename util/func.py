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
        print(f'Môn {subject}: {percentile(diem[subject], score[subject])}')

def higher(data: pd.DataFrame, value):
    'Return the percent of value that is SMALLER than given value'
    temp = data[data >= value].count()
    return f'{temp}'

def custom_combi(custom: dict, sbd = None):
    '''Return a graph of a custom combination of subjects
    Param:
    custom: a dictionary containing subjects and their multipliers
    sbd
    '''
    valid = {}
    for val in custom.keys():
        if val in subjects_lower:
            try:
                valid[val] = int(custom[val])
            except ValueError:
                pass
    custom_data = sum([(diem[subjects[subjects_lower.index(val)]] * valid[val]) for val in valid.keys()])
    data_to_plot = custom_data.value_counts().sort_index()
    title = ", ".join([f'{subjects[subjects_lower.index(val)]} (hệ số {valid[val]})' for val in valid.keys()])
    fig = px.line(x = data_to_plot.index.sort_values(), y = data_to_plot, template="ggplot2", title=(f'Điểm thi môn {title}'))
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
    

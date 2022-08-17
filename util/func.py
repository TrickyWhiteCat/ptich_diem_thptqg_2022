import pandas as pd
import numpy as np
from data import *
import plotly.express as px
from dash import html, dcc
import plotly.graph_objects as go

def tra_diem(sbd: str, data = data, diem = diem):
    return diem.loc[data['SBD'] == int(sbd)].iloc[0].dropna()

def percentile(data: pd.DataFrame, value):
    'Return the percent of value that is SMALLER than given value'
    temp = data[data < value].count() / data.count()
    return f'{temp:.2%}'

def percentile_all_subjects(data: pd.DataFrame, diem, id: str):
    score = tra_diem(id)
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
        d = tra_diem(sbd)
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

def create_graph(sbd = 0, mon = '', graph_type = 'bar', df_diem = diem):
    if sbd:
        d = tra_diem(sbd = sbd)
        personal_sj = df_diem[d.index] # Remove NaN scores

        if not mon and mon not in personal_sj:
            raise KeyError(f'Thí sinh có số báo danh {sbd} không thi môn {mon}')
    
        data_to_plot = personal_sj[mon].value_counts().sort_index()
    
    else:
        data_to_plot = df_diem[mon].value_counts().sort_index()
    
    if graph_type == 'line':
        fig = px.line(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {mon}', template="ggplot2")
    else:
        fig = px.bar(x = data_to_plot.index.sort_values(), y = data_to_plot, title=f'Điểm thi môn {mon}', template="ggplot2")
    
    fig.update_layout(xaxis_title='Điểm', yaxis_title='Số thí sinh')
    
    if sbd:
        info = html.Div(className='info', children = 
                    [html.H6(f'Điểm của bạn: {d[mon]:.2f}'),
                    html.H6(f'''Điểm của bạn cao hơn {percentile(data=df_diem[mon], value = d[mon])} các thí sinh khác! Chỉ có {higher(data=df_diem[mon], value = d[mon])} thí sinh có điểm cao hơn bạn!'''),
                    ])
        
    else:
        info = html.Div(className='info',
                        children = [
                            html.H6(f'Điểm trung bình: {df_diem[mon].mean():.2f}'),
                            html.H6(f'Số điểm nhiều thí sinh đạt được nhất: {diem[mon].mode().iloc[0]}'),
                            html.H6(f'Độ lệch chuẩn: {df_diem[mon].std():.2f}'),
                        ])


    return (html.Div(className = 'fig_container',
                    children=[
                        dcc.Graph(figure=fig, className='graph'),
                        info,
                        ]))

def bang_diem(sbd):
    d = tra_diem(sbd)
    return html.Table(
        children=[
            html.Tr(className='subjects', children=
                [html.Th(className = 'subject', children = subject) for subject in d.index]),
            html.Tr(className = 'scores', children=
                [html.Td(className = 'score', children = score) for score in d.values])
                ])

def diem_theo_tinh(ma_tinh, diem = diem, sbd = SBD):
    return diem.loc[SBD // 1000000 == int(ma_tinh)]

def count_cao_hon_hoac_bang(muc_diem, mon, df_diem = diem, percent = False):
    if isinstance(mon, dict):
        custom_data = sum([(df_diem[subjects[subjects_lower.index(val)]] * mon[val]) for val in mon.keys()])
    else:
        try:
            custom_data = df_diem[mon]
        except KeyError:
            custom_data = df_diem[subjects[subjects_lower.index(mon)]]
    res = custom_data.loc[custom_data >= muc_diem].dropna().count()
    if percent:
        np.seterr('ignore')
        return np.nan_to_num(res/custom_data.count()) * 100
    return res

def choropleth_map(mon, muc_diem, percent = True, region = tinh):

    location_str = 'trên cả nước' if region == 'all' else 'tại miền Bắc' if region == 'bac' else 'tại miền Nam' if region == 'nam' else 'tại miền Trung'
    regions = {'bac': bac, 'nam': nam, 'trung': trung, 'all': tinh}
    region = regions[region] # Du lieu dau vao la 1 str

    diem_moi_tinh = pd.concat([region, region[0].map(lambda x: count_cao_hon_hoac_bang(muc_diem = muc_diem, mon = mon, df_diem = diem_theo_tinh(x), percent=percent))], axis = 1)
    diem_moi_tinh.columns = ['id', 'name', 'value']

    fig = go.Figure(data=
                    go.Choropleth(
                        geojson=vn_map,
                        locations = diem_moi_tinh['id'],
                        featureidkey='properties.id',
                        z=diem_moi_tinh['value'],
                        text=diem_moi_tinh['name'],
                        colorscale='blugrn',
                        colorbar_title = 'Phần trăm (%)' if percent else 'Số lượng (người)'))

    fig.update_geos(fitbounds = 'locations', visible = False)

    if isinstance(mon, dict): # Hiển thị tổ hợp nếu `mon` là 1 dictionary
        if list(mon.values())[0] in subjects:
            sjs = ", ".join([f'{val} (hệ số {mon[val]})' for val in mon.keys()])
        else:
            sjs = ", ".join([f'{subjects[subjects_lower.index(val)]} (hệ số {mon[val]})' for val in mon.keys()])
    fig.update_layout(title_text=f'{"Số lượng" if not percent else "Tỉ lệ"} thí sinh đạt mức điểm cao hơn hoặc bằng {muc_diem} {f"trong tổ hợp {sjs}" if isinstance(mon, dict) else f"ở môn {mon}" if mon in subjects else f"ở môn {subjects[subjects_lower.index(mon)]}"} {location_str}')

    return html.Div(className='choropleth-container',
                    children=[
                        dcc.Graph(figure=fig)])

def choropleth_w_slider(to_hop, muc_diem = 0, id_obj = None, percent = True, region = 'all'):
    '''A wrapper containing a slider controlling `muc_diem` and a choropleth_map'''

    # Get the max possible score
    if isinstance(to_hop, dict):
        max_score = 10 * sum([val for val in to_hop.values()])
    if isinstance(to_hop, str):
        max_score = 10
    else: TypeError(f'to_hop must be either string or dictionary. Got {type(to_hop)} instead')

    if not muc_diem:
        muc_diem = max_score/2

    container = html.Div(id = {'type':'choro-w-slider', 'index':id_obj, 'subject':str(to_hop).replace("\'", "\"")}, #json strings need to be started with " instead of '
                        className='choro-w-slider',
                        children=[
                            html.Div(children = [
                                'Chọn cách tính số lượng',
                                dcc.RadioItems(
                                    className = 'opt', 
                                    options=[
                                                {
                                                    'label':html.Div(children='Tỉ lệ'),
                                                    'value':True
                                                },
                                                {
                                                    'label':html.Div(children='Tổng'),
                                                    'value':False
                                                }
                                ],
                                value = True,
                                id = {'type': 'percent_sum', 'index':id_obj}),
                            ]),
                            html.Div(children = [
                                'Chọn vùng miền',
                                dcc.RadioItems(children = 'Chọn vùng miền',
                                    className = 'opt', 
                                    options=[
                                                {
                                                    'label':html.Div(children='Miền Bắc'),
                                                    'value':'bac'
                                                },
                                                {
                                                    'label':html.Div(children='Miền Trung'),
                                                    'value':'trung'
                                                },
                                                {
                                                    'label':html.Div(children='Miền Nam'),
                                                    'value':'nam'
                                                },
                                                {
                                                    'label':html.Div(children='Toàn quốc'),
                                                    'value':'all'
                                                },
                                                ],
                                value = 'all',
                                id = {'type': 'region', 'index':id_obj}),]),
                            choropleth_map(mon = to_hop, muc_diem = muc_diem, percent = percent, region = region),
                            dcc.Slider(min = 0,
                                        max = max_score,
                                        step = None,
                                        id={'type': 'slider', 'index': id_obj},
                                        value=max_score/2,
                                        included=True),
                            dcc.Input(value=max_score/2,
                                    id = {'type':'slider-input', 'index': id_obj},
                                    type='number')
                            ]) 
    return container

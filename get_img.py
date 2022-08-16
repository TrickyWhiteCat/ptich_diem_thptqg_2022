import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go 

import util

from data import *


def choropleth_map(mon, muc_diem, percent = True, region = 'all'):

    location_str = 'trên cả nước' if region == 'all' else 'tại miền Bắc' if region == 'bac' else 'tại miền Nam' if region == 'nam' else 'tại miền Trung'
    regions = {'bac': bac, 'nam': nam, 'trung': trung, 'all': tinh}
    region = regions[region] # Du lieu dau vao la 1 str

    diem_moi_tinh = pd.concat([region, region[0].map(lambda x: util.count_cao_hon_hoac_bang(muc_diem = muc_diem, mon = mon, percent=percent, ma_sgd = x))], axis = 1).fillna(0)
    diem_moi_tinh.columns = ['id', 'name', 'value']
    title = f'{"Số lượng" if not percent else "Tỉ lệ"} thí sinh đạt mức điểm cao hơn hoặc bằng {muc_diem:.2f} {f"trong tổ hợp {sjs}" if isinstance(mon, dict) else f"ở môn {mon}" if mon in subjects else f"ở môn {subjects[subjects_lower.index(mon)]}"} {location_str}'
    
    fig = go.Figure(data=
                    go.Choropleth(
                        geojson=vn_map,
                        locations = diem_moi_tinh['id'],
                        featureidkey='properties.id',
                        z=diem_moi_tinh['value'],
                        text=diem_moi_tinh['name'],
                        colorscale='blugrn',
                        colorbar_title = 'Phần trăm (%)' if percent else 'Số lượng (người)',
                        ))
    
    fig.update_geos(fitbounds = 'locations', visible = False)

    if isinstance(mon, dict): # Hiển thị tổ hợp nếu `mon` là 1 dictionary
        if list(mon.values())[0] in subjects:
            sjs = ", ".join([f'{val} (hệ số {mon[val]})' for val in mon.keys()])
        else:
            sjs = ", ".join([f'{subjects[subjects_lower.index(val)]} (hệ số {mon[val]})' for val in mon.keys()])
    fig.update_layout(
        title_text=f'{"Số lượng" if not percent else "Tỉ lệ"} thí sinh đạt mức điểm cao hơn hoặc bằng {muc_diem:.2f} {f"trong tổ hợp {sjs}" if isinstance(mon, dict) else f"ở môn {mon}" if mon in subjects else f"ở môn {subjects[subjects_lower.index(mon)]}"} {location_str}',
        margin=dict(l=0,r=0,b=0,t=50),
        width = 1680,
        height = 1050
    )
    return fig

def get_img(subj):
    try:
        os.mkdir(f'images/{subj}')
    except FileExistsError:
        pass
    for val in np.linspace(0, 10, 1001):
        fig = choropleth_map(mon = subj, muc_diem=val, percent=False, region = 'all')
        fig.write_image(f"images/{subj}/count_{int(val * 100):04d}.png")
        print(f'{subj}:{val/10:.1%}')
def main():
    from multiprocessing import Process
    NUM_SUBJECTS = len(subjects_lower) # 1 thread per subject

    for subj in subjects_lower:
        args = [subj]
        if len(args) != 1:
            raise AssertionError(f'Current {args=}')
        p = Process(target=get_img, args=args)
        p.start()

if __name__ == '__main__':
    main()
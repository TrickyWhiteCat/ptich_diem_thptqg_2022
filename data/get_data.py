import numpy as np
import pandas as pd
import unidecode
import json

data = pd.read_csv(r"data/total.csv", low_memory=False)

SBD = data['SBD']
diem = data.drop(columns=['SBD', 'Tên', 'Ngày Sinh', 'Giới tính'])

info = pd.DataFrame([diem.median(), diem.mode().iloc[0], diem.mean(numeric_only=True).round(2)], index=('Median', 'Mode', 'Mean'))
subjects = tuple(diem.columns)
subjects_lower = tuple([unidecode.unidecode(sj).lower() for sj in subjects])

# Load file geojson chua cac tinh tren ban do VN
with open(r'data/diaphantinh.geojson', encoding='utf8') as f:
    vn_map = json.load(f)

# DataFrame chua ma so giao duc va ten tinh
tinh = pd.DataFrame([[tinh['properties']["id"], tinh['properties']["ten_tinh"]] for tinh in vn_map['features']])
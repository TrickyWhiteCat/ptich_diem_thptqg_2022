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

# Chia cac mien:
bac = pd.read_pickle(r'data/map/bac.gz')
trung = pd.read_pickle(r'data/map/trung.gz')
nam = pd.read_pickle(r'data/map/nam.gz')
tinh = pd.read_pickle(r'data/map/tinh.gz')
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
tinh = []

# Chia cac mien:

## Lay ma so giao duc cua cac tinh o moi mien
id_bac = (8, 13, 62, 23, 7, 14, 5, 6, 11, 10, 9, 12, 15, 18, 17, 19, 24, 1, 21, 3, 22, 25, 27, 26, 16)
id_tru = (28, 29, 30, 31, 32, 33, 4, 34, 35, 37, 39, 41, 45, 47, 36, 38, 40, 63, 42)
id_nam = (43, 44, 48, 46, 52, 2, 49, 50, 51, 56, 57, 58, 54, 64, 59, 60, 61, 55, 53)

## Chia cac tinh vao cac mien
bac = []
trung = []
nam = []

for val in vn_map['features']:
    id_ = val['properties']["id"]
    name = val['properties']["ten_tinh"]
    pack = [id_, name]
    
    tinh.append(pack)
    if id_ in id_bac:
        bac.append(pack)
    elif id_ in id_tru:
        trung.append(pack)
    else:
        nam.append(pack)

tinh, bac, trung, nam = map(pd.DataFrame, [tinh, bac, trung, nam])
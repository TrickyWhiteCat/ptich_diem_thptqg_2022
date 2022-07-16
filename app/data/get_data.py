import numpy as np
import pandas as pd
import unidecode

data = pd.read_csv(r"app\data\total.csv", low_memory=False)

sbd = data['SBD']
diem = data.drop(columns=['SBD', 'Tên', 'Ngày Sinh', 'Giới tính'])

info = pd.DataFrame([diem.median(), diem.mode().iloc[0], diem.mean(numeric_only=True).round(2)], index=('Median', 'Mode', 'Mean'))
subjects = tuple(diem.columns)
subjects_lower = tuple([unidecode.unidecode(sj).lower().replace(' ', '%20') for sj in subjects])
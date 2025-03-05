# 4.1 Exercise 1: Column information
import pandas as pd
import json
import pickle


df = pd.read_csv('proj1_ex01.csv')

columns_info = []

for column in df.columns:
    missing_val_percentage = df[column].isnull().mean()

    data_type = df[column].dtype

    if data_type == 'int64':
        data_type_str = 'int'
    elif data_type == 'float64':
        data_type_str = 'float'
    else:
        data_type_str = 'other'

    columns_info.append({
        "name": column,
        "missing": missing_val_percentage,
        "type": data_type_str
    })

with open('proj1_ex01_fields.json', 'w') as json_file:
    json.dump(columns_info, json_file, indent=4)


# 4.2 Exercise 2: Value statistics

import pandas as pd
import json

df = pd.read_csv('proj1_ex01.csv')

stats = df.describe(include='all').to_dict()

for col, values in stats.items():
    for key, value in values.items():
        if pd.isna(value):
            stats[col][key] = None

with open('proj1_ex02_stats.json', 'w') as json_file:
    json.dump(stats, json_file, indent=4)


# 4.3 Exercise 3: Column names
print("4.3 Exercise 3: Column names")
df.columns = df.columns.str.replace('[^A-Za-z0-9_ ]', '', regex=True).str.lower().str.replace(' ', '_')
pd.set_option('display.max_columns', None)
print(df)
df.to_csv('proj1_ex03_columns.csv', index=False)

# 4.4 Exercise 4: Output formats

df.to_excel('proj1_ex04_excel.xlsx', index=False)
df.to_json('proj1_ex04_json.json', orient="records")
df.to_pickle('proj1_ex04_pickle.pkl')




# 4.5 Exercise 5: Selecting rows and columns
print("4.5 Exercise 5: Selecting rows and column")
import pandas as pd
import numpy as np

df = pd.read_pickle('proj1_ex05.pkl')

selected_columns = df.iloc[:, 1:3]
selected_columns.fillna(np.nan, inplace=True)
selected_columns = selected_columns.fillna('')

selected_rows = selected_columns[selected_columns.index.astype(str).str.startswith('v')].copy()

selected_rows.fillna(np.nan, inplace=True)
selected_rows = selected_rows.fillna('')

with open('proj1_ex05_table.md', 'w') as f:
    f.write(selected_rows.to_markdown())


print(df)


# 4.6 Exercise 6: Flattening data

import pandas as pd
import json

print("4.6 Exercise 6: Flattening data\n")

with open('proj1_ex06.json', 'r') as file:
    data = json.load(file)

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

flattened_data = [flatten_dict(entry) for entry in data]

df = pd.DataFrame(flattened_data)

df.to_pickle("proj1_ex06_pickle.pkl")
print(df)

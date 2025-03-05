import pickle
import pandas as pd
import numpy as np
import re
import csv
pd.set_option('display.max_columns', None)

# 3.1 Exercise 1: Load the file

def detect_separator(filename):
    with open(filename, 'r') as file:
        dialect = csv.Sniffer().sniff(file.read(1024))
        return dialect.delimiter

def detect_decimal_separator(filename):
    with open(filename, 'r') as file:
        sample_data = file.read(1024)
        dialect = csv.Sniffer().sniff(sample_data)
        detected_separator = dialect.delimiter
        decimal_separator = getattr(dialect, 'decimal', ',')  # Ustawiam domyślny separator dziesiętny na ','
        # Jeśli wykryty separator to przecinek, ustawiam separator dziesiętny na kropkę
        if detected_separator == ',':
            decimal_separator = '.'
        decimal_pattern = re.compile(r'\d+[' + re.escape(decimal_separator) + ']\d+')  # Wzorzec liczby z separatorem dziesiętnym
        match = decimal_pattern.search(sample_data)
        if match:
            return decimal_separator
        else:
            return '.'  # Jeśli nie znaleziono, ustawiam separator dziesiętny na kropke

separator = detect_separator('proj2_data.csv')
print("Detected separator:", separator)

decimal_sep = detect_decimal_separator('proj2_data.csv')
if decimal_sep:
    print("Detected decimal separator:", decimal_sep)
else:
    print("Decimal separator not detected.")

initial_df = pd.read_csv("proj2_data.csv", sep=separator, decimal=decimal_sep)

initial_df.to_pickle('proj2_ex01.pkl')

print("3.1 Initial_df:\n", initial_df)

for column in initial_df.columns:
    for index, value in initial_df[column].items():
        print(f"Type of value at ({index}, {column}): {type(value)}")


# 3.2 Exercise 2: Value scale
with open("proj2_scale.txt", "r") as file:
    scale_values = [line.strip() for line in file]

copy_of_df = initial_df.copy()
print("3.2 Copy_of_df before:\n", copy_of_df)
for column in copy_of_df.columns:
    if set(copy_of_df[column].unique()).issubset(scale_values):
        copy_of_df[column] = copy_of_df[column].map({value: index + 1 for index, value in enumerate(scale_values)})


copy_of_df.to_pickle('proj2_ex02.pkl')

with open('proj2_ex02.pkl', 'rb') as file:
    zawartosc = pickle.load(file)

print("Copy_of_df after:\n ", zawartosc)


# 3.3 Exercise 3: Categories

updated_df = initial_df.copy()
with open('proj2_scale.txt', 'r') as file:
    scale_values = [line.strip() for line in file]

for column in updated_df.columns:
    if set(updated_df[column].unique()).issubset(scale_values):
        updated_df[column] = pd.Categorical(updated_df[column], categories=scale_values)

updated_df.to_pickle('proj2_ex03.pkl')
print("3.3 Updated df:\n", updated_df)
print(updated_df.dtypes)


# 3.4 Exercise 4: Number extraction

def extract_number(text):
    pattern = r'(\-?[0-9]+(?:[.,][0-9]+)?)'
    match = re.search(pattern, str(text))
    if match:
        return match.group()
    else:
        return np.nan

numeric_df = initial_df.map(extract_number)

extracted_df = initial_df.mask(pd.isna(numeric_df))
extracted_df = extracted_df.dropna(axis=1, how='all')

extracted_df.to_pickle("proj2_ex04.pkl")

print("DataFrame with extracted numbers:")
print(extracted_df)


# 3.5 Exercise 5: One-hot encoding

initial_df = pd.read_pickle('proj2_ex01.pkl')

def contains_only_small_letters(text):
    return bool(re.match('^[a-z]+$', str(text)))

print("Initial_df: \n", initial_df)
selected_columns = []
for column in initial_df.columns:
    if (initial_df[column].dtype == 'object' and
        len(initial_df[column].unique()) <= 10 and
        all(map(contains_only_small_letters, initial_df[column])) and
        not set(initial_df[column]).issubset(scale_values)):
        selected_columns.append(column)

for col in selected_columns:
    one_hot_encoded_df = pd.get_dummies(initial_df[col], prefix='', prefix_sep='')
    file_name = f'proj2_ex05_{selected_columns.index(col) + 1}.pkl'
    one_hot_encoded_df.to_pickle(file_name)

print("Liczba:\n", len(selected_columns) + 1)
print("Zawartosc:\n", selected_columns)

for i in range(1, len(selected_columns) + 1):
    with open(f"proj2_ex05_{i}.pkl", "rb") as file:
        opened5 = pickle.load(file)

    print("Content of file: \n", opened5)

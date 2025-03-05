import pandas as pd
import json
pd.set_option('display.max_columns', None)

# Exercise 1: Load data

data1 = pd.read_json("proj3_data1.json")
print("data1:\n", data1)
data2 = pd.read_json("proj3_data2.json")
print("data2:\n", data2)
data3 = pd.read_json("proj3_data3.json")
print("data3:\n", data3)
all_data = pd.concat([data1, data2, data3], ignore_index=True)
print("all_data:\n", all_data)
all_data.to_json("proj3_ex01_all_data.json")


# Exercise 2: Missing values

missing_values = all_data.isnull().sum()
print("missing_values:\n", missing_values)
missing_values = missing_values[missing_values > 0]
print("")
print("missing_values:\n", missing_values)
missing_values.to_csv("proj3_ex02_no_nulls.csv", header=False)

# Exercise 3: Applying functions
with open("proj3_params.json", "r") as f:
    params = json.load(f)

all_data['description'] = all_data[params['concat_columns']].apply(lambda x: ' '.join(x), axis=1)
all_data.to_json("proj3_ex03_descriptions.json")
print("all_data:\n", all_data)

# Exercise 4: Joining datasets

more_data = pd.read_json("proj3_more_data.json")
print("more_data:\n", more_data)
print("all_data:\n", all_data)
joined_data = pd.merge(all_data, more_data, on=params['join_column'], how='left')
joined_data.to_json("proj3_ex04_joined.json")
print("joined_data:\n", joined_data)


# Exercise 5: Iterating over DataFrames

for index, row in joined_data.iterrows():
    description = row['description'].replace(' ', '_').lower()
    filename = f"proj3_ex05_{description}.json"
    row.drop('description').to_json(filename)
    with open(filename, "r") as file:
        data = json.load(file)
        print(f"\nZawartość pliku {filename}:")
        print(data)

int_columns = params['int_columns']

for index, row in joined_data.iterrows():
    description = row['description'].replace(' ', '_').lower()
    int_row = row.copy()
    for col in int_columns:
        int_row[col] = int(row[col]) if not pd.isnull(row[col]) else None
    filename = f"proj3_ex05_int_{description}.json"
    int_row.drop('description').to_json(filename)
    with open(filename, "r") as file:
        data = json.load(file)
        print(f"\nZawartość pliku {filename}:")
        print(data)



# Exercise 6: Aggregation

aggregations = params['aggregations']
agg_results = {}
for col, func in aggregations:
    if func == 'min':
        agg_results[f"min_{col}"] = joined_data[col].min()
    elif func == 'max':
        agg_results[f"max_{col}"] = joined_data[col].max()
    elif func == 'mean':
        agg_results[f"mean_{col}"] = joined_data[col].mean()

with open("proj3_ex06_aggregations.json", "w") as f:
    json.dump(agg_results, f)

print("agg_results:\n", agg_results)

# Exercise 7: Grouping

#print("df_ex7:\n", joined_data)
grouping_column = params['grouping_column']

print(joined_data)
print(joined_data.info)
print(joined_data.dtypes)
numerical_columns = [col for col in joined_data.columns if joined_data[col].dtype in ['int64', 'float64']]
print("numerical_columns:\n", numerical_columns)
grouped_data = joined_data.groupby(grouping_column)
print("grouped_data:\n", grouped_data)
mean_values = grouped_data[numerical_columns].mean()
print("mean_values:\n", mean_values)
mean_values_filtered = mean_values[grouped_data.size() > 1]
print("mean_values_filtered:\n", mean_values_filtered)
print(mean_values_filtered.info)
print(mean_values_filtered.dtypes)
mean_values_filtered.to_csv("proj3_ex07_groups.csv", header=True, index=True)


# Exercise 8: Reshaping data

pivot_index = params['pivot_index']
pivot_columns = params['pivot_columns']
pivot_values = params['pivot_values']
id_vars = params['id_vars']

pivot_df = joined_data.pivot_table(index=pivot_index, columns=pivot_columns, values=pivot_values, aggfunc='max')
pivot_df.to_pickle("proj3_ex08_pivot.pkl")
print("pivot_df:\n", pivot_df)

melted_df = pd.melt(joined_data, id_vars=id_vars, var_name='variable', value_name='value')
melted_df.to_csv("proj3_ex08_melt.csv", header=True, index=False)
print("melted_df:\n", melted_df)

df = pd.read_csv("proj3_statistics.csv")

pivot_df = pd.wide_to_long(df, stubnames=["Audi", "BMW", "Volkswagen", "Renault"], i="Country", j="Year", sep="_")

pivot_df.reset_index(inplace=True)

print(pivot_df)
pivot_df["Country_Year"] = "('" + pivot_df["Country"] + "', " + pivot_df["Year"].astype(str) + ")"
df_output = pivot_df[["Country_Year", "Audi", "BMW", "Volkswagen", "Renault"]]
print(df_output)
df_output = df_output.set_index("Country_Year")
df_output.index.name = None
df_output.to_csv("proj3_ex08_stats.pkl")




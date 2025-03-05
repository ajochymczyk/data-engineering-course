import sqlite3
import pandas as pd
import bz2
import shutil
import subprocess
import os
import pickle

con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()

# Exercise 1: Basic counting
result_ex01 = cur.execute("SELECT COUNT(DISTINCT detector_id) FROM readings;").fetchall()
df_ex01 = pd.DataFrame(result_ex01, columns=['detector_count'])
df_ex01.to_pickle("proj6_ex01_detector_no.pkl")

# Exercise 2: Some stats for the detectors
result_ex02 = cur.execute("""
    SELECT 
        detector_id, 
        COUNT(*) AS count, 
        MIN(starttime) AS min_starttime, 
        MAX(starttime) AS max_starttime 
    FROM readings 
    WHERE count IS NOT NULL 
    GROUP BY detector_id;
""").fetchall()
df_ex02 = pd.DataFrame(result_ex02, columns=['detector_id', 'count(count)', 'min(starttime)', 'max(starttime)'])
df_ex02.to_pickle("proj6_ex02_detector_stat.pkl")

# Exercise 3: Moving Window
result_ex03 = cur.execute("""
    SELECT 
        detector_id, 
        count, 
        LAG(count) OVER (ORDER BY starttime) AS prev_count 
    FROM readings 
    WHERE detector_id = 146 
    LIMIT 500;
""").fetchall()
df_ex03 = pd.DataFrame(result_ex03, columns=['detector_id', 'count', 'prev_count'])
df_ex03.to_pickle("proj6_ex03_detector_146_lag.pkl")

# Exercise 4: Window
result_ex04 = cur.execute("""
    SELECT 
        detector_id, 
        count, 
        SUM(count) OVER (ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 9 FOLLOWING) AS window_sum 
    FROM readings 
    WHERE detector_id = 146 
    LIMIT 500;
    
    
""").fetchall()
df_ex04 = pd.DataFrame(result_ex04, columns=['detector_id', 'count', 'window_sum'])
df_ex04.to_pickle("proj6_ex04_detector_146_sum.pkl")

con.close()

print(pd.read_pickle("proj6_ex01_detector_no.pkl"))
print(pd.read_pickle("proj6_ex02_detector_stat.pkl"))
print(pd.read_pickle("proj6_ex03_detector_146_lag.pkl"))
print(pd.read_pickle("proj6_ex03_detector_146_lag.pkl"))

import os

import pandas as pd
dir = os.listdir('./static/data_dir')

my_list = []
for csv in dir:
    data = pd.read_csv("./static/data_dir/" + csv)
    my_list.append(data)

df = pd.concat(my_list)
df.to_csv('test.csv')
print(df)
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from datetime import datetime

df = pd.read_csv('aqua_master - Copy.csv')

print(df.head())

prices = [float(x.strip('$')) for x in df['price']]

date= [x.split('-') for x in df['date']]

x_axis = []

for i in date:
	print(i[0])
	print(i[1])
	x_axis.append(float(str(i[0]) +'.'+ str(i[1])))


date_time_obj = [datetime.strptime(x, "%Y%m%d-%H%M") for x in df['date']]

plt.scatter(date_time_obj, prices)
plt.xticks(rotation=90)
plt.xlim(min(date_time_obj), max(date_time_obj))
plt.show()

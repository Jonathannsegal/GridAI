import pandas
import time
import datetime

df = pandas.read_csv("./neo4j/import/Smart Meter Data.xlsx - FeederA_Smart Meter Data.csv")
i = 0
for str in df["Time:datetime"]:
    d = time.strptime(str,"%m/%d/%y %I:%M %p")
    df.at[i,"Time:datetime"] = time.strftime("%Y-%m-%dT%H:%M", d)
    i+=1
df.to_csv('data.csv',index=False,header=True)

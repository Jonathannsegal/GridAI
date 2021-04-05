import pandas
import time
import datetime

#df = pandas.read_csv("./neo4j/import/Smart Meter Data.xlsx - FeederA_Smart Meter Data.csv")
df = pandas.read_csv("./neo4j/import/data.csv")
# for str in df["Time:datetime"]:
#     d = time.strptime(str,"%m/%d/%y %I:%M %p")
#     df.at[i,"Time:datetime"] = time.strftime("%Y-%m-%dT%H:%M", d)
#     i+=1
#df = df.transpose()
#_header = df.iloc[0]
#df = df[1:]

#for i, val in enumerate(new_header):
#    new_header[i] = val + ':double'

#df.columns = new_header

#for i, val in enumerate(df['bus']):
#    df['bus'][i] = val.replace(':double', '')
print(df)

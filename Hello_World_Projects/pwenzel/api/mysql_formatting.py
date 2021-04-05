import pandas as pd
import time as t
import datetime as dt


meter_fp = ("/home/ubuntu/Downloads/Smart Meter Data.xlsx")
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
smart_meter_b = pd.read_excel(meter_fp, sheet_name = 'FeederB_Smart Meter Data', header = 0, index_col = 0)
smart_meter_c = pd.read_excel(meter_fp, sheet_name = 'FeederC_Smart Meter Data', header = 0, index_col = 0)

smart_meter_a.index.rename('Date', inplace=True)
smart_meter_a.to_csv('sma.csv')
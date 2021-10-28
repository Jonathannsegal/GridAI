
import pandas as pd
import time as t
import datetime as dt

# Formats Smart Meter Data to be loaded into MySQL table
meter_fp = ("./system_data/Smart Meter Data.xlsx")
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
smart_meter_b = pd.read_excel(meter_fp, sheet_name = 'FeederB_Smart Meter Data', header = 0, index_col = 0)
smart_meter_c = pd.read_excel(meter_fp, sheet_name = 'FeederC_Smart Meter Data', header = 0, index_col = 0)

meter = smart_meter_a.join(smart_meter_b)
meter = meter.join(smart_meter_c)
meter.index.rename('Date', inplace=True)
meter.to_csv('./mysql/meter.csv')
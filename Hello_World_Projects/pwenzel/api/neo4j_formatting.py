#!/usr/bin/env python
# coding: utf-8

# In[86]:


import pandas as pd
import time as t
import datetime as dt


# In[87]:


trans_fp = ("./240 Node Test System Element Data.xlsx")


# In[88]:


transformers_3p = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 1, index_col = 0, usecols = [0,4,5,6,7,8], nrows = 53)
transformers_1p = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 58, index_col = 0, usecols = [0,5,6,7,8,9], nrows = 2)
transformers_1pct = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 65, index_col = 0, usecols = [0,3,13,14,15,16,17,18], nrows = 139)
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols = [1,2,3,4], nrows = 16)
feeder_B_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols=[8,9,10,11], nrows = 57)
feeder_C_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols = [15,16,17,18], nrows = 160)
bus_coord = pd.read_excel(trans_fp, sheet_name = 'Bus Coordinates', header = 0, index_col = 0,usecols = [0,1,2], nrows = 240)


# In[89]:


cols = []
for val in transformers_1p.columns:
    cols.append(val + (':double'))
transformers_1p.columns = cols
cols = []
for val in transformers_3p.columns:
    cols.append(val + ':double')
transformers_3p.columns = cols
cols = []
for val in transformers_1pct.columns:
    cols.append(val + (':double'))
transformers_1pct.columns = cols


# In[90]:


prev_bus = []
bus_x = []
bus_y = []
for str in transformers_3p.index:
    bus_num = str[2:6]
    if bus_num[0] == '1':
        prev_node = feeder_A_line_Segments.loc[int(bus_num)]['Bus A']
        prev_bus.append(prev_node)
    if bus_num[0] == '2':
        prev_node = feeder_B_line_Segments.loc[int(bus_num)]['Bus A.1']
        prev_bus.append(prev_node)
    if bus_num[0] == '3':
        prev_node = feeder_C_line_Segments.loc[int(bus_num)]['Bus A.2']
        prev_bus.append(prev_node)
    bus = 'bus' + bus_num
    bus_x.append(bus_coord.loc[bus]['X'])
    bus_y.append(bus_coord.loc[bus]['Y'])
transformers_3p['Previous Bus:int'] = prev_bus
prev_bus = []
transformers_3p['X:double'] = bus_x
transformers_3p['Y:double'] = bus_y
bus_x = []
bus_y = []
for str in transformers_1p.index:
    bus_num = str[2:6]
    if bus_num[0] == '1':
        prev_node = feeder_A_line_Segments.loc[int(bus_num)]['Bus A']
        prev_bus.append(prev_node)
    if bus_num[0] == '2':
        prev_node = feeder_B_line_Segments.loc[int(bus_num)]['Bus A.1']
        prev_bus.append(prev_node)
    if bus_num[0] == '3':
        prev_node = feeder_C_line_Segments.loc[int(bus_num)]['Bus A.2']
        prev_bus.append(prev_node)
    bus = 'bus' + bus_num
    bus_x.append(bus_coord.loc[bus]['X'])
    bus_y.append(bus_coord.loc[bus]['Y'])
transformers_1p['Previous Bus:int'] = prev_bus
prev_bus = []
transformers_1p['X:double'] = bus_x
transformers_1p['Y:double'] = bus_y
bus_x = []
bus_y = []
for str in transformers_1pct.index:
    bus_num = str[2:6]
    if bus_num[0] == '1':
        prev_node = feeder_A_line_Segments.loc[int(bus_num)]['Bus A']
        prev_bus.append(prev_node)
    if bus_num[0] == '2':
        prev_node = feeder_B_line_Segments.loc[int(bus_num)]['Bus A.1']
        prev_bus.append(prev_node)
    if bus_num[0] == '3':
        prev_node = feeder_C_line_Segments.loc[int(bus_num)]['Bus A.2']
        prev_bus.append(prev_node)
    bus = 'bus' + bus_num
    bus_x.append(bus_coord.loc[bus]['X'])
    bus_y.append(bus_coord.loc[bus]['Y'])
transformers_1pct['Previous Bus:int'] = prev_bus
transformers_1pct['X:double'] = bus_x
transformers_1pct['Y:double'] = bus_y
bus_x = []
bus_y = []


# In[91]:


transformers_3p.rename_axis('BusID:ID', inplace=True)
transformers_3p.index


# In[92]:


transformers_1p.rename_axis('BusID:ID',inplace=True)


# In[93]:


transformers_1pct.rename_axis('BusID:ID',inplace=True)


# In[94]:


transformers_3p.to_csv('transformers_3p.csv')
transformers_1p.to_csv('transformers_1p.csv')
transformers_1pct.to_csv('transformers_1pct.csv')


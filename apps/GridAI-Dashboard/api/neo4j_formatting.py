import pandas as pd
import time as t
import datetime as dt

# This file formats data to be quickly manually imported to Neo4j database

# Define file for necessary data (Transformer properties, Coordinates, Line Data)
trans_fp = ("./system_data/240 Node Test System Element Data.xlsx")

# Read data into dataframes to be processed. Change parameters as necessary for specific dataset

# Three Phase
transformers_3p = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 1, index_col = 0, usecols = [0,4,5,6,7,8], nrows = 53)
# Single Phase
transformers_1p = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 58, index_col = 0, usecols = [0,5,6,7,8,9], nrows = 2)
# Single Phase Center Tapped
transformers_1pct = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 65, index_col = 0, usecols = [0,4,13,14,15,16,17,18], nrows = 139)
# Others
transformers_others= pd.read_excel(trans_fp, sheet_name = 'Bus Coordinates', header = 0, index_col = 0, usecols = [0,1,2], nrows = 240)

# Line Data
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols = [1,2,3,4], nrows = 16)
feeder_B_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols=[8,9,10,11], nrows = 57)
feeder_C_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols = [15,16,17,18], nrows = 160)

# X,Y Coordinates
bus_coord = pd.read_excel(trans_fp, sheet_name = 'Bus Coordinates', header = 0, index_col = 0,usecols = [0,1,2], nrows = 240)


# Append variable type to column names as required by Neo4j for importing dataset
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

transformers_others.rename_axis('BusID:ID', inplace=True)
transformers_others.reset_index(inplace=True)
transformers_others.columns = ['BusID:ID','X:double', 'Y:double']

# Parse Line Data to identify previous transformer connections in grid network and parse X,Y coordinates
prev_bus = []
bus_x = []
bus_y = []
for temp in transformers_3p.index:
    bus_num = temp[2:6]
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
transformers_3p['X:double'] = bus_x
transformers_3p['Y:double'] = bus_y

prev_bus = []
bus_x = []
bus_y = []
for temp in transformers_1p.index:
    bus_num = temp[2:6]
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
transformers_1p['X:double'] = bus_x
transformers_1p['Y:double'] = bus_y

prev_bus = []
bus_x = []
bus_y = []
for temp in transformers_1pct.index:
    bus_num = temp[2:6]
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

prev_bus = []
for str in transformers_others['BusID:ID'].values:
    bus_num = str[-4:]
    if (bus_num[0] == '1') and (int(bus_num) in feeder_A_line_Segments.index.values):
        prev_node = feeder_A_line_Segments.loc[int(bus_num)]['Bus A']
        prev_bus.append(prev_node)
    elif (bus_num[0] == '2') and (int(bus_num) in feeder_B_line_Segments.index.values):
        prev_node = feeder_B_line_Segments.loc[int(bus_num)]['Bus A.1']
        prev_bus.append(prev_node)
    elif (bus_num[0] == '3') and (int(bus_num) in feeder_C_line_Segments.index.values):
        prev_node = feeder_C_line_Segments.loc[int(bus_num)]['Bus A.2']
        prev_bus.append(prev_node)
    else:
        prev_bus.append(0)
transformers_others['Previous Bus:int'] = prev_bus



# Move BusID from index to column to import as property in Neo4j
transformers_3p.rename_axis('BusID:ID', inplace=True)
transformers_1p.rename_axis('BusID:ID',inplace=True)
transformers_1pct.rename_axis('BusID:ID',inplace=True)
transformers_3p.reset_index(inplace=True)
transformers_1p.reset_index(inplace=True)
transformers_1pct.reset_index(inplace=True)

# Clean BusIDs of any whitespace that may have been accidentally parsed
for i, rows in transformers_3p.iterrows():
    transformers_3p.at[i,'BusID:ID'] = transformers_3p.at[i,'BusID:ID'].strip()

for i, rows in transformers_1p.iterrows():
    transformers_1p.at[i,'BusID:ID'] = transformers_1p.at[i,'BusID:ID'].strip()

for i, rows in transformers_1pct.iterrows():
    transformers_1pct.at[i,'BusID:ID'] = transformers_1pct.at[i,'BusID:ID'].strip()

# Filter out duplicate BusIDs from 'Other' transformers 
for i, row in transformers_others.iterrows():
    bus_id = 'T_'+ row['BusID:ID'][-4:]
    if bus_id in transformers_3p['BusID:ID'].values or bus_id in transformers_1p['BusID:ID'].values or bus_id in transformers_1pct['BusID:ID'].values:
        transformers_others.drop([i], inplace=True)
    else:
        transformers_others.at[i,'BusID:ID'] = transformers_others.at[i,'BusID:ID'].replace('bus','T_')
transformers_others.reset_index(drop=True, inplace=True)

# Initialize all other features that are required for ML models
transformers_3p['Year:int'] = 0
transformers_1p['Year:int'] = 0
transformers_1pct['Year:int'] = 0
transformers_3p['Month:int'] = 0
transformers_1p['Month:int'] = 0
transformers_1pct['Month:int'] = 0
transformers_3p['Day:int'] = 0
transformers_1p['Day:int'] = 0
transformers_1pct['Day:int'] = 0
transformers_3p['Hour:int'] = 0
transformers_1p['Hour:int'] = 0
transformers_1pct['Hour:int'] = 0
transformers_3p['CurrVal:double'] = 0
transformers_3p['PrevNode Val:double'] = 0
transformers_3p['PrevVal:double'] = 0
transformers_1p['CurrVal:double'] = 0
transformers_1p['PrevNode Val:double'] = 0
transformers_1p['PrevVal:double'] = 0
transformers_1pct['CurrVal:double'] = 0
transformers_1pct['PrevNode Val:double'] = 0
transformers_1pct['PrevVal:double'] = 0
transformers_others['Year:int'] = 0
transformers_others['Month:int'] = 0
transformers_others['Day:int'] = 0
transformers_others['Hour:int'] = 0
transformers_others['CurrVal:double'] = 0
transformers_others['PrevNode Val:double'] = 0
transformers_others['PrevVal:double'] = 0




transformers_3p.to_csv('./neo4j/import/transformers_3p.csv')
transformers_1p.to_csv('./neo4j/import/transformers_1p.csv')
transformers_1pct.to_csv('./neo4j/import/transformers_1pct.csv')
transformers_others.to_csv('./neo4j/import/transformers_others.csv')



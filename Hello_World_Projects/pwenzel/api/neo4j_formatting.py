import pandas as pd
import time as t
import datetime as dt



trans_fp = ("/home/ubuntu/Downloads/240 Node Test System Element Data.xlsx")
meter_fp = ("/home/ubuntu/Downloads/Smart Meter Data.xlsx")
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
smart_meter_b = pd.read_excel(meter_fp, sheet_name = 'FeederB_Smart Meter Data', header = 0, index_col = 0)
smart_meter_c = pd.read_excel(meter_fp, sheet_name = 'FeederC_Smart Meter Data', header = 0, index_col = 0)




transformers_3p = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 1, index_col = 0, usecols = [0,4,5,6,7,8], nrows = 53)
transformers_1p = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 58, index_col = 0, usecols = [0,5,6,7,8,9], nrows = 2)
transformers_1pct = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 65, index_col = 0, usecols = [0,3,13,14,15,16,17,18], nrows = 139)
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols = [1,2,3,4], nrows = 16)
feeder_B_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols=[8,9,10,11], nrows = 57)
feeder_C_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 1,usecols = [15,16,17,18], nrows = 160)
bus_coord = pd.read_excel(trans_fp, sheet_name = 'Bus Coordinates', header = 0, index_col = 0,usecols = [0,1,2], nrows = 240)



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
prev_bus = []
transformers_3p['X:double'] = bus_x
transformers_3p['Y:double'] = bus_y
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
prev_bus = []
transformers_1p['X:double'] = bus_x
transformers_1p['Y:double'] = bus_y
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
bus_x = []
bus_y = []


transformers_3p.rename_axis('BusID:ID', inplace=True)
transformers_1p.rename_axis('BusID:ID',inplace=True)
transformers_1pct.rename_axis('BusID:ID',inplace=True)
transformers_3p.reset_index(inplace=True)
transformers_1p.reset_index(inplace=True)
transformers_1pct.reset_index(inplace=True)

three_phase = []
three_phase_prev = []
three_phase_prevNode = []
single_phase = []
single_phase_prev = []
single_phase_prevNode = []
single_phase_ct = []
single_phase_ctprev = []
single_phase_ctprevNode = []
dates = smart_meter_a.index
for bus in transformers_3p['BusID:ID']:
    bus_num = bus[2:6]
    prevBus = str(transformers_3p.loc[transformers_3p['BusID:ID'] == bus]['Previous Bus:int'].values[0])
    if bus_num[0] == '1':
        three_phase.append(smart_meter_a.loc[dates[100]]['Bus ' + bus_num])
        three_phase_prev.append(smart_meter_a.loc[dates[99]]['Bus ' + bus_num])
        three_phase_prevNode.append(smart_meter_a.loc[dates[100]]['Bus ' + prevBus])
    elif bus_num[0] == '2':
        three_phase.append(smart_meter_b.loc[dates[100]]['Bus ' + bus_num])
        three_phase_prev.append(smart_meter_b.loc[dates[99]]['Bus ' + bus_num])
        three_phase_prevNode.append(smart_meter_b.loc[dates[100]]['Bus ' + prevBus])
    else:
        three_phase.append(smart_meter_c.loc[dates[100]]['Bus ' + bus_num])
        three_phase_prev.append(smart_meter_c.loc[dates[99]]['Bus ' + bus_num])
        three_phase_prevNode.append(smart_meter_c.loc[dates[100]]['Bus ' + prevBus])
for bus in transformers_1p['BusID:ID']:
    bus_num = bus[2:6]
    prevBus = str(transformers_1p.loc[transformers_1p['BusID:ID'] == bus]['Previous Bus:int'].values[0])
    if bus_num[0] == '1':
        single_phase.append(smart_meter_a.loc[dates[100]]['Bus ' + bus_num])
        single_phase_prev.append(smart_meter_a.loc[dates[99]]['Bus ' + bus_num])
        single_phase_prevNode.append(smart_meter_a.loc[dates[100]]['Bus ' + prevBus])
    elif bus_num[0] == '2':
        single_phase.append(smart_meter_b.loc[dates[100]]['Bus ' + bus_num])
        single_phase_prev.append(smart_meter_b.loc[dates[99]]['Bus ' + bus_num])
        single_phase_prevNode.append(smart_meter_b.loc[dates[100]]['Bus ' + prevBus])
    else:
        single_phase.append(smart_meter_c.loc[dates[100]]['Bus ' + bus_num])
        single_phase_prev.append(smart_meter_c.loc[dates[99]]['Bus ' + bus_num])
        single_phase_prevNode.append(smart_meter_c.loc[dates[100]]['Bus ' + prevBus])
for bus in transformers_1pct['BusID:ID']:
    bus_num = bus[2:6]
    prevBus = str(transformers_1pct.loc[transformers_1pct['BusID:ID'] == bus]['Previous Bus:int'].values[0])
    if bus_num[0] == '1':
        single_phase_ct.append(smart_meter_a.loc[dates[100]]['Bus ' + bus_num])
        single_phase_ctprev.append(smart_meter_a.loc[dates[99]]['Bus ' + bus_num])
        single_phase_ctprevNode.append(smart_meter_a.loc[dates[100]]['Bus ' + prevBus])
    elif bus_num[0] == '2':
        single_phase_ct.append(smart_meter_b.loc[dates[100]]['Bus ' + bus_num])
        single_phase_ctprev.append(smart_meter_b.loc[dates[99]]['Bus ' + bus_num])
        single_phase_ctprevNode.append(smart_meter_b.loc[dates[100]]['Bus ' + prevBus])
    else:
        single_phase_ct.append(smart_meter_c.loc[dates[100]]['Bus ' + bus_num])
        single_phase_ctprev.append(smart_meter_c.loc[dates[99]]['Bus ' + bus_num])
        single_phase_ctprevNode.append(smart_meter_c.loc[dates[100]]['Bus ' + prevBus])


transformers_3p['Year:int'] = dates[100].year
transformers_1p['Year:int'] = dates[100].year
transformers_1pct['Year:int'] = dates[100].year
transformers_3p['Month:int'] = dates[100].month
transformers_1p['Month:int'] = dates[100].month
transformers_1pct['Month:int'] = dates[100].month
transformers_3p['Day:int'] = dates[100].day
transformers_1p['Day:int'] = dates[100].day
transformers_1pct['Day:int'] = dates[100].day
transformers_3p['Hour:int'] = dates[100].hour
transformers_1p['Hour:int'] = dates[100].hour
transformers_1pct['Hour:int'] = dates[100].hour
transformers_3p['CurrVal:double'] = three_phase
transformers_3p['PrevNode Val:double'] = three_phase_prevNode
transformers_3p['PrevVal:double'] = three_phase_prev
transformers_1p['CurrVal:double'] = single_phase
transformers_1p['PrevNode Val:double'] = single_phase_prevNode
transformers_1p['PrevVal:double'] = single_phase_prev
transformers_1pct['CurrVal:double'] = single_phase_ct
transformers_1pct['PrevNode Val:double'] = single_phase_ctprevNode
transformers_1pct['PrevVal:double'] = single_phase_ctprev



transformers_3p.to_csv('transformers_3p.csv')
transformers_1p.to_csv('transformers_1p.csv')
transformers_1pct.to_csv('transformers_1pct.csv')



import xlrd
import pandas as pd
import random
#File Path
trans_fp = ("/home/jrmerkel/Documents/Python/491/240 Node Test System Element Data.xlsx")
meter_fp = ("/home/jrmerkel/Documents/Python/491/Smart Meter Data.xlsx")
random.seed(0)
#Read in the SPCT data
singleCenterTapped= pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 65, index_col = 0, usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], nrows = 140)
#Reads in the line segments
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 0,usecols = [0,1,2,3,4,5], nrows = 16)

newList = []
indexList = []
#Smart meter A
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
#Process each pus
for index, value in smart_meter_a.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:
        #locate if this station is a transformer
        bus_attr = singleCenterTapped.loc['T_' + bus_num]
        if(bus_attr is None):
            break
        else:
            # try and grab the previous bus
            line = feeder_A_line_Segments[feeder_A_line_Segments['Bus B'] == int(bus_num)]
            prev_bus = line.get('Bus A')

            cont = 1
    except KeyError:
        #do nothing the transformer is not in our dataframe
        
        pass
    if(cont == 1):
        print(bus_num)
        indexList.append(bus_num)
        prev_val = 0
        for busIndex, busValue in value.items():
  
            
            newListItem = []
            #Static node data
            newListItem.append(bus_attr.loc['Voltage rating of\nWinding 1 (kV)'])
            #   %R
            newListItem.append(bus_attr.loc[' %R1'])
            newListItem.append(bus_attr.loc[' %R2'])
            newListItem.append(bus_attr.loc[' %R3'])
            # %x
            newListItem.append(bus_attr.loc[' %X12'])
            newListItem.append(bus_attr.loc[' %X13'])
            newListItem.append(bus_attr.loc[' %X23'])
            #timestamp year
            newListItem.append(busIndex.year)
            #timestamp month
            newListItem.append(busIndex.month)
            #TimeStamp Day
            newListItem.append(busIndex.day)
            #TimeStamp hour (lowest level of precision)
            newListItem.append(busIndex.hour)
            #Value
            rand_val = random.randint(0,15)
            if(rand_val == 1):
                #Power Failure
                busValue = 0
                newListItem.append(busValue)
                newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(1)
                prev_val = busValue
            elif (rand_val == 2):
                #Power Spike
                busValue = busValue * 2
                newListItem.append(busValue)
                newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(2)
                prev_val = busValue
            else:
                #Normal Data
                newListItem.append(busValue)
                newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(0)
                prev_val = busValue
            newList.append(newListItem)

feeder_B_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, usecols = [7,8,9,10,11,12], nrows = 57)
#Feeder B
smart_meter_b = pd.read_excel(meter_fp, sheet_name = 'FeederB_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_b.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:

        #locate if this station is a transformer
        bus_attr = singleCenterTapped.loc['T_' + bus_num]
        if(bus_attr is None):
            break
        else:
            # try and grab the previous bus
            line = feeder_B_line_Segments[feeder_B_line_Segments['Bus B.1'] == int(bus_num)]
            prev_bus = line.get('Bus A.1')

            cont = 1
    except KeyError:
        #do nothing the transformer is not in our dataframe
        pass

    if(cont == 1):
        print(bus_num)
        indexList.append(bus_num)
        prev_val = 0
        for busIndex, busValue in value.items():
  

            newListItem = []
            #Static Node Data
            newListItem.append(bus_attr.loc['Voltage rating of\nWinding 1 (kV)'])
            #   %R
            newListItem.append(bus_attr.loc[' %R1'])
            newListItem.append(bus_attr.loc[' %R2'])
            newListItem.append(bus_attr.loc[' %R3'])
            # %x
            newListItem.append(bus_attr.loc[' %X12'])
            newListItem.append(bus_attr.loc[' %X13'])
            newListItem.append(bus_attr.loc[' %X23'])
            #timestamp year
            newListItem.append(busIndex.year)
            #timestamp month
            newListItem.append(busIndex.month)
            #TimeStamp Day
            newListItem.append(busIndex.day)
            #TimeStamp hour (lowest level of precision)
            newListItem.append(busIndex.hour)
            #Value
            rand_val = random.randint(0,15)
            if(rand_val == 1):
                #Power Failure
                busValue = 0
                newListItem.append(busValue)
                newListItem.append(smart_meter_b.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(1)
                prev_val = busValue
            elif (rand_val == 2):
                #Power Spike
                busValue = busValue * 2
                newListItem.append(busValue)
                newListItem.append(smart_meter_b.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(2)
                prev_val = busValue
            else:
                #Normal Data
                newListItem.append(busValue)
                newListItem.append(smart_meter_b.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(0)
                prev_val = busValue
            newList.append(newListItem)

feeder_C_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, usecols = [14,15,16,17,18,19], nrows = 160)
#Feeder C
smart_meter_c = pd.read_excel(meter_fp, sheet_name = 'FeederC_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_c.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:
        #locate if this station is a transformer
        bus_attr = singleCenterTapped.loc['T_' + bus_num]
        if(bus_attr is None):
            break
        else:
            # try and grab the previous bus
            line = feeder_C_line_Segments[feeder_C_line_Segments['Bus B.2'] == int(bus_num)]
            prev_bus = line.get('Bus A.2')

            cont = 1
    except KeyError:
        #do nothing the transformer is not in our dataframe
        
        pass
    if(cont == 1):
        print(bus_num)
        indexList.append(bus_num)
        prev_val = 0
        for busIndex, busValue in value.items():
  
            newListItem = []
            #static transformer data
            newListItem.append(bus_attr.loc['Voltage rating of\nWinding 1 (kV)'])
            #   %R
            newListItem.append(bus_attr.loc[' %R1'])
            newListItem.append(bus_attr.loc[' %R2'])
            newListItem.append(bus_attr.loc[' %R3'])
            # %x
            newListItem.append(bus_attr.loc[' %X12'])
            newListItem.append(bus_attr.loc[' %X13'])
            newListItem.append(bus_attr.loc[' %X23'])
            #timestamp year
            newListItem.append(busIndex.year)
            #timestamp month
            newListItem.append(busIndex.month)
            #TimeStamp Day
            newListItem.append(busIndex.day)
            #TimeStamp hour (lowest level of precision)
            newListItem.append(busIndex.hour)
            #Value
            rand_val = random.randint(0,15)
            if(rand_val == 1):
                #Power Failure
                busValue = 0
                newListItem.append(busValue)
                newListItem.append(smart_meter_c.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(1)
                prev_val = busValue
            elif (rand_val == 2):
                #Power Spike
                busValue = busValue * 2
                newListItem.append(busValue)
                newListItem.append(smart_meter_c.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(2)
                prev_val = busValue
            else:
                #Normal Data
                newListItem.append(busValue)
                newListItem.append(smart_meter_c.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(0)
                prev_val = busValue
            newList.append(newListItem)

#SPCT Anomaly datasheet export
df = pd.DataFrame(newList, columns = ['kVA rating', '%R1', '%R2', '%R3', '%X12','%X13','%X23','Year', 'Month', 'Day', 'Hour', 'Current Value','Prev Node', 'Prev Time', 'Anomaly'])
df.to_csv('Anomaly_SPCT.csv')
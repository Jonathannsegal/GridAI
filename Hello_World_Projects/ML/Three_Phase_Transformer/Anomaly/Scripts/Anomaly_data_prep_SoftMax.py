import xlrd
import pandas as pd
import random
#Specify datapaths
trans_fp = ("./240 Node Test System Element Data.xlsx")
meter_fp = ("./Smart Meter Data.xlsx")
random.seed(0)

#Read in TP data
three_phase= pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 1, index_col = 0, usecols = [0,1,2,3,4,5,6,7,8], nrows = 54)
#Reads in the line segments
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 0,usecols = [0,1,2,3,4,5], nrows = 16)

newList = []
indexList = []
#Read in smart meter A
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_a.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:
        #locate if this station is a transformer
        bus_attr = three_phase.loc['T_' + bus_num]
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
            #Get Static Node Data
            newListItem.append(bus_attr.loc['Primary voltage rating (kV)'])
            #   %R
            newListItem.append(bus_attr.loc['Secondary voltage rating (kV)'])
            # %x
            newListItem.append(bus_attr.loc['kVA rating (kVA)'])
            newListItem.append(bus_attr.loc[' %R'])
            newListItem.append(bus_attr.loc[' %X'])
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
                #normal Data
                newListItem.append(busValue)
                newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
                newListItem.append(prev_val)
                newListItem.append(0)
                prev_val = busValue
            newList.append(newListItem)

feeder_B_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, usecols = [7,8,9,10,11,12], nrows = 57)
# Feeder B
smart_meter_b = pd.read_excel(meter_fp, sheet_name = 'FeederB_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_b.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:

        #locate if this station is a transformer
        bus_attr = three_phase.loc['T_' + bus_num]
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
            #Get Static Node data
            newListItem.append(bus_attr.loc['Primary voltage rating (kV)'])
            #   %R
            newListItem.append(bus_attr.loc['Secondary voltage rating (kV)'])
            # %x
            newListItem.append(bus_attr.loc['kVA rating (kVA)'])
            newListItem.append(bus_attr.loc[' %R'])
            newListItem.append(bus_attr.loc[' %X'])
            #timestamp year
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
# Process Feeder C
smart_meter_c = pd.read_excel(meter_fp, sheet_name = 'FeederC_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_c.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:
        #locate if this station is a transformer
        bus_attr = three_phase.loc['T_' + bus_num]
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
            #Get Static Node Data
            newListItem.append(bus_attr.loc['Primary voltage rating (kV)'])
            #   %R
            newListItem.append(bus_attr.loc['Secondary voltage rating (kV)'])
            # %x
            newListItem.append(bus_attr.loc['kVA rating (kVA)'])
            newListItem.append(bus_attr.loc[' %R'])
            newListItem.append(bus_attr.loc[' %X'])
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
   
#Export to new spreadsheet
df = pd.DataFrame(newList, columns = ['Primary voltage rating (kV)', 'Secondary voltage rating (kV)', 'kVA rating (kVA)', '%R', '%X','Year', 'Month', 'Day', 'Hour', 'Current Value','Prev Node', 'Prev Time', 'Anomaly'])
df.to_csv('Anomaly_TP.csv')
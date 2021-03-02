import xlrd
import pandas as pd
#importing the element system data Just the 3 phase secondary distribution transformer for now
trans_fp = ("/home/ubuntu/Documents/sdmay21-23/Hello_World_Projects/Tensorflow_test/240 Node Test System Element Data.xlsx")
meter_fp = ("/home/ubuntu/Documents/sdmay21-23/Hello_World_Projects/Tensorflow_test/Smart Meter Data.xlsx")
# wb = xlrd.open_workbook(filepath)
# dist_tran_sheet = wb.sheet_by_index(5)

# dist_tran_sheet.cell_value(0,0)
# rows = dist_tran_sheet.nrows
# cols = dist_tran_sheet.ncols

# print(dist_tran_sheet.row_values(2))
#ThreePhtransformers = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 1, index_col = 0, usecols = [0,1,2,3,4,5,6,7,8], nrows = 54)
singleCenterTapped= pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 65, index_col = 0, usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], nrows = 140)
singleCenterTapped.to_csv('tapTest.csv')
#print(x.loc['T_1003'])
#Reads in the line segments
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 0,usecols = [0,1,2,3,4,5], nrows = 16)
feeder_A_line_Segments.to_csv('FeederA')
newList = []
indexList = []
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
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
        current_val = 0
        for busIndex, busValue in value.items():
  
            #Primary voltage rating (kV)
            newListItem = []
            #print(bus_attr.loc['Primary voltage rating (kV)'])
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
            newListItem.append(current_val)
            newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
            newListItem.append(prev_val)
            newListItem.append(busValue)
            prev_val = current_val
            current_val = busValue
            newList.append(newListItem)

feeder_B_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, usecols = [7,8,9,10,11,12], nrows = 57)
feeder_B_line_Segments.to_csv('FeederBTest.csv')
smart_meter_b = pd.read_excel(meter_fp, sheet_name = 'FeederB_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_b.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:
        if(int(bus_num) == 2008):
            print('here')

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
        current_val = 0
        for busIndex, busValue in value.items():
  
            #Primary voltage rating (kV)
            newListItem = []
            #print(bus_attr.loc['Primary voltage rating (kV)'])
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
            newListItem.append(current_val)
            newListItem.append(smart_meter_b.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
            newListItem.append(prev_val)
            newListItem.append(busValue)
            prev_val = current_val
            current_val = busValue
            newList.append(newListItem)
   
    #Primary voltage rating (kV)
    #Secondary voltage rating (kV)
    #kVA rating (kVA)
    # %R
    # %x
feeder_C_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, usecols = [14,15,16,17,18,19], nrows = 160)
feeder_C_line_Segments.to_csv('FeederCTest.csv')
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
        current_val = 0
        for busIndex, busValue in value.items():
  
            #Primary voltage rating (kV)
            newListItem = []
            #print(bus_attr.loc['Primary voltage rating (kV)'])
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
            newListItem.append(current_val)
            newListItem.append(smart_meter_c.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
            newListItem.append(prev_val)
            newListItem.append(busValue)
            prev_val = current_val
            current_val = busValue
            newList.append(newListItem)
   
    #Primary voltage rating (kV)
    #Secondary voltage rating (kV)
    #kVA rating (kVA)
    # %R
    # %x
#should have a new spreadsheet
df = pd.DataFrame(newList, columns = ['kVA rating', '%R1', '%R2', '%R3', '%X12','%X13','%X23','Year', 'Month', 'Day', 'Hour', 'Current Value','Prev Node', 'Prev Time', 'Future Value'])
df.to_csv('Single_Phase_Center_Tap_Future.csv')
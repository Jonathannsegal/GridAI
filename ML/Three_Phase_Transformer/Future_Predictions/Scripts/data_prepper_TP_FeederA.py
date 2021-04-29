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
transformers = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 1, index_col = 0, usecols = [0,1,2,3,4,5,6,7,8], nrows = 54)
#print(x.loc['T_1003'])
#Reads in the line segments
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 0,usecols = [0,1,2,3,4,5], nrows = 16)

newList = []
indexList = []
smart_meter_a = pd.read_excel(meter_fp, sheet_name = 'FeederA_Smart Meter Data', header = 0, index_col = 0)
for index, value in smart_meter_a.items():
    # Get last 4 characters which are the bus number
    bus_num = index[-4:]
    cont = 0
    try:
        #locate if this station is a transformer
        bus_attr = transformers.loc['T_' + bus_num]
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

        indexList.append(bus_num)
        prev_val = 0
        current_val = 0
        for busIndex, busValue in value.items():

            #print(bus_attr)
            #print('HERE')
            # print("index")
            # print(busIndex)
            # print("value")
            # print(busValue)   
            #Primary voltage rating (kV)
            #print(bus_attr.loc['Primary voltage rating (kV)'])
            newListItem = []
           # print(newListItem)
            #print(bus_attr.loc['Primary voltage rating (kV)'])
            newListItem.append(bus_attr.loc['Primary voltage rating (kV)'])
          #  print(newListItem)
            #Secondary voltage rating (kV)
            newListItem.append(bus_attr.loc['Secondary voltage rating (kV)'])
           # print(newListItem)
            #kVA rating (kVA)
            newListItem.append(bus_attr.loc['kVA rating (kVA)'])
            #print(newListItem)
            #   %R
            newListItem.append(bus_attr.loc[' %R'])
            #print(newListItem)
            # %x
            newListItem.append(bus_attr.loc[' %X'])
           # print(newListItem)
            #timestamp year
            newListItem.append(busIndex.year)
            #timestamp month
            newListItem.append(busIndex.month)
            #TimeStamp Day
            newListItem.append(busIndex.day)
            #TimeStamp hour (lowest level of precision)
            newListItem.append(busIndex.hour)
            #print(newListItem)
            #Value
            newListItem.append(current_val)
            newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
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
df = pd.DataFrame(newList, columns = ['Primary voltage rating (kV)', 'Secondary voltage rating (kV)', 'kVA rating (kVA)', '%R', '%X','Year', 'Month', 'Day', 'Hour', 'Value','Prev Node', 'Prev Time','Future Value'])
df.to_csv('test.csv')

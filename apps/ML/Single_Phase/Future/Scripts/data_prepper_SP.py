import xlrd
import pandas as pd
#Specify Datapaths
trans_fp = ("/home/ubuntu/Documents/sdmay21-23/Hello_World_Projects/Tensorflow_test/240 Node Test System Element Data.xlsx")
meter_fp = ("/home/ubuntu/Documents/sdmay21-23/Hello_World_Projects/Tensorflow_test/Smart Meter Data.xlsx")

#Read in single phase data
transformers = pd.read_excel(trans_fp, sheet_name = 'Distribution Transformer', header = 58, index_col = 0, usecols = [0,1,2,3,4,5,6,7,8,9,10], nrows = 2)

#Reads in the line segments
feeder_A_line_Segments = pd.read_excel(trans_fp, sheet_name = 'Line Data', header = 1, index_col = 0,usecols = [0,1,2,3,4,5], nrows = 16)

newList = []
indexList = []
#Read in the smart meter A data
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

            newListItem = []
            #Static Data
            newListItem.append(bus_attr.loc['Primary voltage rating (kV)'])
            #Secondary voltage rating (kV)
            newListItem.append(bus_attr.loc['Secondary voltage rating (kV)'])
            #kVA rating (kVA)
            newListItem.append(bus_attr.loc['kVA rating (kVA)'])
            #   %R
            newListItem.append(bus_attr.loc[' %R'])
            # %x
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
            newListItem.append(current_val)
            newListItem.append(smart_meter_a.loc[busIndex].loc['Bus ' + str(prev_bus.array[0])])
            newListItem.append(prev_val)
            newListItem.append(busValue)
            #keep track of old value
            prev_val = current_val
            current_val = busValue
            newList.append(newListItem)
   

#Data is ready (SP only has feeder A)
df = pd.DataFrame(newList, columns = ['Primary voltage rating (kV)', 'Secondary voltage rating (kV)', 'kVA rating (kVA)', '%R', '%X','Year', 'Month', 'Day', 'Hour', 'Value','Prev Node', 'Prev Time','Future Value'])
df.to_csv('test.csv')
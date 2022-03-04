import os,re,telnetlib,time
import json

def get_ddp_batch(command):
    HOST = "192.168.50.113"
    PORT = "7000"
    TIMEOUT = 5

    #tableIndex, dataIndex, dataLength = getIndexByCommand(command)
    retID, tableIndex = getIdByCommand(command)
    #For Test
    #retID = "6781"
    #retID = "677B"

    cmd_ddp = "getDdpBatchData " + str(tableIndex)
    
    #cmd_ddp = "123"

    retBatchData = ""

    #retBatchData = "FE CB 30 00 8E 00 00 00 02 00 8A 67 A2 67 7B 01 01 0D"

    # set High Altitude to 1  # For Test
    #retBatchData = "FE CB 30 00 8E 00 00 00 02 00 8A 67 A2 67 7B 01 01 67 1A 01 00 67 36 01 00 67 7D 02 00 00 67 7C 02 00 00 67 7E 02 14 00 67 AF 01 00 67 4A 01 01 67 4D 01 03 67 4E 01 06 67 51 01 05 67 52 02 FF FF 67 53 02 0A 00 67 63 01 05 67 64 01 03 67 70 01 00 67 73 02 00 00 67 80 01 04 67 81 01 01 67 1B 01 00 67 42 01 00 67 4F 01 00 67 1F 01 00 67 43 01 00 67 44 01 13 67 75 01 00 67 76 02 01 00 67 0A 02 00 00 67 82 02 00 00 67 83 02 00 00 67 7E 02 14 00 0D"
    # set High Altitude to 0  # For Test
    #retBatchData = "FE CB 30 00 8E 00 00 00 02 00 8A 67 A2 67 7B 01 01 67 1A 01 00 67 36 01 00 67 7D 02 00 00 67 7C 02 00 00 67 7E 02 14 00 67 AF 01 00 67 4A 01 01 67 4D 01 03 67 4E 01 06 67 51 01 05 67 52 02 FF FF 67 53 02 0A 00 67 63 01 05 67 64 01 03 67 70 01 00 67 73 02 00 00 67 80 01 04 67 81 01 00 67 1B 01 00 67 42 01 00 67 4F 01 00 67 1F 01 00 67 43 01 00 67 44 01 13 67 75 01 00 67 76 02 01 00 67 0A 02 00 00 67 82 02 00 00 67 83 02 00 00 67 7E 02 14 00 0D"

    '''
    ### For Test ###
    retBatchData = "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 32 "
    retBatchData += "00 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "AA BB CC DD EE FF GG HH II JJ "
    retBatchData += "01 22 33 44 55 66 77 88 99 10 "

    '''

    with telnetlib.Telnet(HOST, PORT, TIMEOUT) as tn:

        print("write:" + cmd_ddp)
        #tn.write("getDdpBatchData 1" + b"\r\n")

        tn.write(cmd_ddp.encode('ascii') + b"\r\n")   # only 17 bytes  ,apk get 17 bytes
        #tn.write(cmd_ddp.encode('ascii'))   ### no return value, apk get all result

        #tn.write(cmd_ddp.encode('ascii') + b"\n")   # means 'carriage return'
        #tn.write(cmd_ddp.encode('ascii') + b"\r")   # means 'line break' or more commonly 'new line'

        time.sleep(1)  # need this one

        retBatchData = tn.read_very_eager().decode('ascii')
        print("read retBatchData:" + retBatchData)

    #return parsing_value(dataIndex, retBatchData, dataLength) # old case
    myHashMap = transferToHashMap(retBatchData)
    return searchValueById(retID, myHashMap)
'''
def parsing_value(dataIndex, retBatchData, dataLength):
    print("dataIndex:" + str(dataIndex) + ",dataLength:"+ str(dataLength))
    #print("BatchData:" + retBatchData)
    retData = ""

    if dataIndex !=  None:
        arrayData = retBatchData.strip().split(" ")
        print("arrayData length:" + str(len(arrayData)))

        if (dataIndex) < len(arrayData):
            #print(arrayData[dataIndex])
            for i in range(dataIndex, dataIndex + dataLength, 1):
                retData = retData + arrayData[i] + " "

            return retData.strip()  # remove leading and trailing whitespaces.
        else:
            print("\n>>> ERROR:dataIndex is not available:" + str(dataIndex))
            return None
    else:
        return None
'''
'''
def getIndexByCommand(command):
    jsonFile = "AllBatchCommandTable.json"
    retValue = None
    retTableNum = None
    retLength = None

    with open(jsonFile, "r") as readit:
        data = json.load(readit)

        for table in data['BatchCommandTableList']:
            tempIndex = 0
            tableIndex = table['tableNumber']
            for cmd in table['tableData']:
                tempIndex = tempIndex + cmd['dataLength'] + 3       # 3 means 'ID(2 byte) and length(1 byte)'
                #print("cmd:" + cmd['command'] + " ,index=" + str(tempIndex))
                if command == cmd['command']:
                    #print("Get this tempIndex!!!!!:" + str(tempIndex))
                    retValue = tempIndex
                    retValue += 13 # header length offset
                    retTableNum = tableIndex
                    retLength = cmd['dataLength']
                    return retTableNum, (retValue-1), retLength
                    
    print("\n>>> ERROR:Command not found(" + jsonFile + "):" + command + "\n")
    return retTableNum, retValue, retLength # None
'''
def getIdByCommand(command):
    jsonFile = "AllBatchCommandTable.json"
    retID = None
    retTable = None

    with open(jsonFile, "r") as readit:
        data = json.load(readit)
        for table in data['BatchCommandTableList']:
            tableIndex = table['tableNumber']
            for cmd in table['tableData']:
                if command == cmd['command']:
                    retID = cmd['commandIDHex']
                    retTable = tableIndex
                    print("Found retID:" + retID + ",retTable:" + str(retTable))
                    return retID, retTable

    print("\n>>> ERROR:Command not found(" + jsonFile + "):" + command + "\n")
    return retID, retTable # None

def searchValueById(retID, myHashMap):
    return myHashMap.get(retID) # Dictionaries

def transferToHashMap(retBatchData):
    retHashMap = {}
    retHashMap["1"] = "Sachin Tendulkar" 

    beginIndex = 13 # header

    arrayData = retBatchData.strip().split(" ")
    print("arrayData length:" + str(len(arrayData))) #149

    i = beginIndex
    while i < len(arrayData)-1:
        key = arrayData[i] + arrayData[i+1]
        #print("key:"+key)
        length = arrayData[i+2]
        #print("length:"+length)

        value = ""
        for j in range(i+3, i+3+int(length), 1):
            value = value + arrayData[j] + " "
        value = value.strip()  # remove leading and trailing whitespaces.
        retHashMap[key] = value
        #print("before i:"+str(i))
        i = i + 3 + int(length)
        #print("after i:"+str(i))
    #print(retHashMap)

    return retHashMap
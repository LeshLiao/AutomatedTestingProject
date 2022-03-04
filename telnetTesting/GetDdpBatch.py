import os,re,telnetlib,time
import json

def get_ddp_batch(command):
    HOST = "192.168.50.113"
    PORT = "7000"
    TIMEOUT = 2 

    tableIndex, dataIndex = getIndexByCommand(command)

    cmd_ddp = "getDdpBatchData " + str(tableIndex)
    
    #cmd_ddp = "123"

    retBatchData = ""
    
    ### For Test ###
    retBatchData = "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "11 22 33 44 55 66 77 88 99 10 "
    retBatchData += "AA BB CC DD EE FF GG HH II JJ "
    retBatchData += "00 22 33 44 55 66 77 88 99 10 "

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
    '''
    return parsing_value(dataIndex, retBatchData)

def parsing_value(dataIndex, retBatchData):
    print("dataIndex:" + str(dataIndex))
    print("BatchData:" + retBatchData)

    if dataIndex !=  None:
        arrayData = retBatchData.split(" ")
        print("arrayData length:" + str(len(arrayData)))

        if (dataIndex) < len(arrayData):
            #print(arrayData[dataIndex])
            return arrayData[dataIndex]
        else:
            print("\n>>> ERROR:dataIndex is not available:" + str(dataIndex))
            return None
    else:
        return None

def getIndexByCommand(command):
    jsonFile = "AllBatchCommandTable.json"
    retValue = None
    retTableNum = None

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
                    retTableNum = tableIndex
                    return retTableNum, (retValue-1)
                    
    print("\n>>> ERROR:Command not found(" + jsonFile + "):" + command + "\n")
    return retTableNum, retValue # None

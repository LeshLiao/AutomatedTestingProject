import os,re,telnetlib,time
import json

# Test
#import struct from telnetlib import DO, DONT, IAC, WILL, WONT, NAWS, SB, SE
#MAX_WINDOW_WIDTH = 65000  # Max Value: 65535
#MAX_WINDOW_HEIGHT = 5000


def get_ddp_batch(command):
   
    HOST = "192.168.50.113"
    PORT = "7000"
    TIMEOUT = 2 

    tableIndex, dataIndex = getIndexByCommand(command)

    #cmd_ddp = "getDdpBatchData " + str(tableIndex)
    
    cmd_ddp = "123"

    retBatchData = ""
    
    ### For Test ###
    #retBatchData = "11 22 33 44 55 66 77 88 99 10 11 12 13 14 15 16 17 18 19 20 21 22 00 24 25 26 27 28 29 30"
    
    with telnetlib.Telnet(HOST, PORT, TIMEOUT) as tn:

        print("write:" + cmd_ddp)
        #tn.write("getDdpBatchData 1" + b"\r\n")
        
        tn.write(cmd_ddp.encode('ascii') + b"\r\n")   # only 17 bytes  ,apk get 17 bytes
        #tn.write(cmd_ddp.encode('ascii'))   ### no return value, apk get all result

        #print("sleep for 1s")
        time.sleep(1)  # need this one

        #retBatchData = tn.read_eager().decode('ascii')
        retBatchData = tn.read_very_eager().decode('ascii')
        print("read retBatchData:" + retBatchData)


    return parsing_value(dataIndex, retBatchData)

def parsing_value(dataIndex, retBatchData):
    print("parsing_value dataIndex:" + str(dataIndex))
    print("parsing_value retBatchData:" + retBatchData)

    if dataIndex !=  None:
        print("parsing_value dataIndex:" + str(dataIndex))
        arrayData = retBatchData.split(" ")
        print("arrayData length:" + str(len(arrayData)))
        
        if (dataIndex-1) < len(arrayData):
            print(arrayData[dataIndex-1])
            return arrayData[dataIndex-1]
        else:
            print("\n>>> ERROR:dataIndex is bigger than arrayData length:" + str(dataIndex))
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
            dataIndex = 0
            tableIndex = table['tableNumber']
            for cmd in table['tableData']:
                dataIndex += cmd['dataLength']
                #print("cmd:" + cmd['command'] + " ,index=" + str(dataIndex))
                if command == cmd['command']:
                    print("Get this dataIndex!!!!!:" + str(dataIndex))
                    retValue = dataIndex
                    retTableNum = tableIndex
                    return retTableNum, retValue
                    
    print("\n>>> ERROR:Command not found(" + jsonFile + "):" + command + "\n")
    return retTableNum, retValue

import parametrize_from_file
import time
import pytest
import json
from Telnet_sender import send_cmd
from GetDdpBatch import get_ddp_batch

# Initial Data 
pytest.myconfig_goto_cmd = ""
pytest.myflag_testcaseIndex = 0
pytest.myflag_skip = True
pytest.myconfig_projectID = "00"

def setup_module():
    with open("test_Telnet.json", "r") as readit:
        data = json.load(readit)
        print("test Suite:" + data['test Suite'])
        print("config_skipTestUntilMet:" + data['config_skipTestUntilMet'])
        pytest.myconfig_goto_cmd = data['config_skipTestUntilMet']

@parametrize_from_file
def test_telnetCommand(test_case, command, telnet_cmd, expectedInterface, expectedDdp):
    pytest.myflag_testcaseIndex += 1
    print('\n\n[%s]\n%s' %(str(pytest.myflag_testcaseIndex), test_case))
    
    # === Arrange ===
    setupBeforeRunATest(test_case, command)

    print("Command:" + command)
    print("Telnet send:" + telnet_cmd)

    # Run test step by step
    #input("Press Enter to continue...")

    # === Act ===
    ret_telnet = send_cmd(pytest.myconfig_projectID, telnet_cmd)
    print("Telnet receive:" + ret_telnet)
    
    time.sleep(1)
    
    ret_Ddp = get_ddp_batch(command)
    print("DDP expected:" + expectedDdp)
    print("DDP return  :" + str(ret_Ddp))
    
    # === Assert ===

    if ret_telnet.find(expectedInterface) == 0:    # If found at begin of ret_telnet
        #if ret_telnet.find("Ok") == 0:                # For Test
        assert True
    else:
        assert False
    
    assert ret_Ddp == expectedDdp


def setupBeforeRunATest(test_case, command):
    if pytest.myconfig_goto_cmd == "":
        pytest.myflag_skip = False
    elif pytest.myconfig_goto_cmd == command:
        pytest.myflag_skip = False

    if pytest.myflag_skip == True or isContainSkip(test_case):
        pytest.skip("=== skip ===")

def isContainSkip(test_case):
    lowercaseStr = test_case.lower()
    if lowercaseStr.find("skip") == 0:
        return True
    else:
        return False
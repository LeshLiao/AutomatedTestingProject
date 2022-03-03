import parametrize_from_file
import time
import pytest
from Telnet_sender import send_cmd
from GetDdpBatch import get_ddp_batch

# Go to specific test case
#pytest.myconfig_goto_cmd = "HighAltitude"

# Run all Test
pytest.myconfig_goto_cmd = ""

# Initial Data 
pytest.myflag_skip = True
pytest.myconfig_projectID = "00"

@parametrize_from_file
def test_telnetCommand(test_case, command, telnet_cmd, expectedTelnet, expectedDdp):
    print('\n\n%s' % test_case)
    
    # === Arrange ===
    setupBeforeRunATest(command)
        
    print("Command:" + command)
    print("Telnet command:" + telnet_cmd)

    # Run test step by step
    #input("Press Enter to continue...")

    # === Act ===
    ret_telnet = send_cmd(pytest.myconfig_projectID, telnet_cmd)
    print("ret_telnet:" + ret_telnet)
    
    time.sleep(1)
    
    ret_Ddp = get_ddp_batch(command)
    print("Get DDP value:" + str(ret_Ddp))

    # === Assert ===

    # If found at begin of ret_telnet
    #if ret_telnet.find(expectedTelnet) == 0: 
    if ret_telnet.find("Ok") == 0: ### For Test ###
        assert True
    else:
        assert False
    
    assert ret_Ddp == expectedDdp


def setupBeforeRunATest(command):
    if pytest.myconfig_goto_cmd == "":
        pytest.myflag_skip = False
    elif pytest.myconfig_goto_cmd == command:
        pytest.myflag_skip = False

    if pytest.myflag_skip == True:
        pytest.skip("=== skip ===")


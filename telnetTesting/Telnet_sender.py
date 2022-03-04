import os,re,telnetlib,time

def send_cmd(projectid, telnet_cmd):
    #HOST = "192.168.50.113"
    #PORT = "9000"
    
    HOST = "172.20.10.3"
    PORT = "5000"
    TIMEOUT = 2

    command = telnet_cmd.replace("XX", projectid)
    
    ### For Test ###
    #return "Ok123"

    with telnetlib.Telnet(HOST, PORT, TIMEOUT) as tn:

        print("telnet write:" + command)
        tn.write(command.encode('ascii') + b"\r\n")

        print("sleep for 1s")
        time.sleep(1)
        
        ret = tn.read_very_eager().decode('ascii')
        print("telnet read:" + ret)

        return ret


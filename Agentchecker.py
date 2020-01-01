#!/usr/bin/env python3
import sys
import socket
import time
import subprocess

timeout = 1 # Since it's an internal network, 1 sec will be enough 

HOST_LIST = sys.argv[1] # path to the file containing the list og hosts or ip addresses of the agents
PORT = sys.argv[2] # the port that the agents are listening on.

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def isOpen(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPv4, SOCK_STREAM for TCP
    s.settimeout(timeout)
    try:
        s.connect((host, int(port))) # try to eatablish a connection with ip/port combination.
        s.shutdown(socket.SHUT_RDWR)  # No exception raised so far, it's safe now to shutdown the connection
        return True
    except:
        return False
    finally:
        s.close()


def pingable(host):    
    ping = subprocess.Popen(
        ["ping", "-c", str(timeout), "-W", str(timeout), host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = ping.communicate()
    if "64 bytes from" in str(out):
       return True
    else:
       return False


with open(HOST_LIST,'r') as f:
    print (f"{bcolors.BOLD} Starting Server/Agent connectivity health check ...")
    for HOST in f:
        HOST = HOST.strip()
        if not HOST:
            break
        elif not pingable(HOST): # check whether the host is online with ping, supposing ICMP is opened through network firewall.
            print (f"{bcolors.WARNING}" + HOST + " ...Ureachable")
        else:
            if isOpen(HOST,PORT): # check if we can connect with the host on the specified port
                print (f"{bcolors.OKGREEN}" + HOST + " ...Sucess")
            else:
                print (f"{bcolors.FAIL}" + HOST + " ...Failed")

#!/usr/bin/env python3
import sys
import socket
import time
import subprocess

timeout = 1 # Since it's an internal network, 1 sec will be enough 

ip_list = sys.argv[1] # path to the file of ip/host list
port = 1234 # change this to the port required i.e the port that agent client lisenting on

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def isOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM). # AF_INET for IPv4, SOCK_STREAM for TCP
    s.settimeout(timeout). 
    try:
        s.connect((ip, int(port))). # try to eatablish a connection with ip/port combination.
        s.shutdown(socket.SHUT_RDWR)  # No exception raised so far, it's safe now to shutdown the connection
        return True
    except:
        return False
    finally:
        s.close()


def pingable(host):    
    ping = subprocess.Popen(
        ["ping", "-c", timeout, "-W", timeout, host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = ping.communicate()
    if "64 bytes from" in str(out):
       return True
    else:
       return False


with open(ip_list,'r') as f:
    print (f"{bcolors.BOLD} Starting Server/Agent connectivity health check ...")
    for ip in f:
        ip = ip.strip()
        if not ip:
            break
        if not pingable(ip): # check whether the host is online with ping, supposing ICMP is opened through network firewall.
            print (f"{bcolors.WARNING}" + ip + " ...Ureachable")
        elif isOpen(ip,port): # check if we can connect with the host on the specified port
            print (f"{bcolors.OKGREEN}" + ip + " ...Sucess")
        else:
            print (f"{bcolors.FAIL}" + ip + " ... Failed")

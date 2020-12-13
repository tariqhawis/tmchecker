#!/usr/bin/env python3
import sys
import socket
import time
import subprocess
import base64
import jwt
import hashlib
import requests
from Crypto.PublicKey import RSA
import json
import urllib3
import getopt
from pprint import pprint

urllib3.disable_warnings()
timeout = 1 # enough for internal network

HOST_LIST = "scan.lst" # The file containing hosts, IP, or MAC addresses of the targets
PORT = "12345" # Listening port in which targets are connected with Trend Micro Officescan/Apex ONE Server
Export = "result.lst" # Scan output stored here
result_list = list()
hostList = list()
adType = "ip"
addr = ""
details = list()
detailSwitch = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_checksum(http_method, raw_url, headers, request_body):
    string_to_hash = http_method.upper() + '|' + raw_url.lower() + '|' + headers + '|' + request_body
    base64_string = base64.b64encode(hashlib.sha256(str.encode(string_to_hash)).digest()).decode('utf-8')
    return base64_string

def create_jwt_token(appication_id, api_key, http_method, raw_url, headers, request_body,
                     iat=time.time(), algorithm='HS256', version='V1'):
    checksum = create_checksum(http_method, raw_url, headers, request_body)
    payload = {'appid': appication_id,
               'iat': iat,
               'version': version,
               'checksum': checksum}
    token = jwt.encode(payload, api_key, algorithm=algorithm).decode('utf-8')
    return token

# Use this region to setup the call info of the TMCM server (server url, application id, api key)
use_url_base = 'https://IP:443' # Trend Micro Control Manager/Apex Central server address
use_application_id = 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
use_api_key = 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx' # API key of Trend Micro CM/AC Server

# This is the path for ProductAgents API
productAgentAPIPath = '/WebApp/API/AgentResource/ProductAgents'
# currently Canonical-Request-Headers will always be empty
canonicalRequestHeaders = ''

#using TrendMicro ApexCentral API to check whether the machine(IP) has an apex agent installed.
def hasTMAgent(host,adType='ip'):
    useQueryString = "?ip_address=" + host
    if adType == 'mac':
        useQueryString = "?mac_address=" + host
    useRequestBody = ''
    jwt_token = create_jwt_token(use_application_id, use_api_key, 'GET',
                              productAgentAPIPath + useQueryString,
                              canonicalRequestHeaders, useRequestBody, iat=time.time())
    headers = {'Authorization': 'Bearer ' + jwt_token}
    r = requests.get(use_url_base + productAgentAPIPath + useQueryString, headers=headers, data=useRequestBody, verify=False)
    if not 'result_content' in r.json() or len(r.json()['result_content']) == 0:
        return False
    return r.json()['result_content']

def checkIP(addr):
    try:
        socket.inet_aton(addr)
    except socket.error:
        return False
    return True


try:
   opts, args = getopt.getopt(sys.argv[1:],"t:a:l:d",["type=","address=","list=","details"])
except getopt.GetoptError:
   print ('TMCheck.py [--type=mac] [--address=[IP]|[MAC]]')
   sys.exit(2)
for opt, arg in opts:
   if opt in ('-t','--type'):
      adType = arg
   elif opt in ('-a','--address'):
      addr = arg
   elif opt in ('-l','--list'):
      HOST_LIST = arg
   elif opt in ('-d','--details'):
      detailSwitch = True

if addr and addr != "":
    if not hasTMAgent(addr,adType): # check if we can connect with the host on the specified port
        print (f"{bcolors.FAIL}" + addr + " ...No Agent")
        result_list.append(addr)
    else:
        if detailSwitch:
           pprint(hasTMAgent(addr,adType))
        print (f"{bcolors.OKGREEN}" + addr + " ...Agent Installed")
else:
    hostList = [line.rstrip('\n') for line in open(HOST_LIST)]
    hostList = dict.fromkeys(hostList)

    for HOST in hostList:
        HOST = HOST.strip()
        if not HOST or HOST == " ":
            continue
        elif not checkIP(HOST) and adType == "ip":
            print(f"{bcolors.WARNING} Wrong IP format in " + HOST_LIST)
            continue

        elif not hasTMAgent(HOST,adType): # check if we can connect with the host on the specified port
            print (f"{bcolors.FAIL}" + HOST + " ...No Agent")
            result_list.append(HOST)
        else:
            if detailSwitch:
               pprint(hasTMAgent(HOST,adType))
            print (f"{bcolors.OKGREEN}" + HOST + " ...Agent Installed")

if Export:
    fh = open(Export,'w')
    fh.writelines(["%s\n" % host  for host in result_list])
    fh.close()
else:
    print("No addresses provided")

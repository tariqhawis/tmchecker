# agentchecker

A simple python script to check a spesific port at a remote machine and return the status.

It is useful for any network/system admin in a business environment that need to troublshoot the connectivity between a server and a long list of agent addresses. Sometime server applications do not give a correct status of a list of agents or you need to do a double checking.

Usage:

Python3 agentchecker.py path/to/host_list port

Example:

Python3 agentchecker.py host_list 1234

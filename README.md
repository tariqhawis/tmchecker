# Trend Micro Officescan/Apex ONE Checker

This python script is useful for automating checking of Officescan/APEX ONE agent existence and whether it is working properly.

## HOW TO USE

The script support check the target by its hostname, IP, and MAC Address.

Moreover, you can provide the bulk of addresses or just one address by its hostname/IP/MAC.

Here are the options from help menu:

``./tmchecker.py [--type=mac] [--address=[IP]|[MAC]]``

--type: To check by target's MAC address, to check by the IP, leave this argument.

--address: To check only one address, To check the bulk of addresses, leave this one and instead fill scan.lst line by line.


### Examples:

1) Check the bulk of targets by IP, fill scan.lst with all your addresses and run:

``./tmchecker.py``

2) Check by the bulk of MACs:

``./tmchecker.py --type=mac

3) ./ 
 
Example:

Python3 agentsdiagnostic.py host_list 1234

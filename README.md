# Trend Micro Officescan/Apex ONE Checker

This python script is useful to automate checking of Officescan/APEX ONE agent, whether installed plus up and running.

# HOW TO USE

This script supports scanning one machine address or bulk of addresses, whether the address provided is a hostname, IP, or MAC.

Here are the options from help menu:

``./tmchecker.py [--type=mac] [--address=[IP]|[MAC]]``

``--type``: Determine the type of address; for MAC Address just type "mac". The default type is IP, so leave this argument in this case.

``--address``: Here provide the target's address. To scan more than one address, fill them in ``scan.lst`` and leave this argument.


# Examples:

## Bulk Check:

* To check a group of addresses, you need to fill them in scan.lst file and only run:

``./tmchecker.py``

* For a group of Mac addresses, fill the addresses in ``scan.lst`` file then run this instead:

``./tmchecker.py --type=mac``


In either case, the results will be printed on your terminal screen as well as on the ``result.lst``, which can be easily shared to do actions afterward.


## Single Check:

* To check a single address, add the parameter ``--address`` as follows:

``./tmchecker.py --address=192.168.1.1``

> Note that you don't need to specify the type for ip addresses, since it's chosen by default.


* For Mac address, run this instead:

``./tmchecker.py --type=mac --address=66:66:66:66:66:66``

 
# Wants to Contribute?

If you have any suggestion to improve this script, feel free to contact me at [Github tmchecker issues](https://github.com/tariqhawis/tmchecker/issues)

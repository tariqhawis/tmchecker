# Trend Micro Officescan/Apex ONE Checker

This python script is useful to automate checking of Officescan/APEX ONE agent, whether installed plus up and running.


# Installation

* Clone this repository to your machine:

``git clone https://github.com/tariqhawis/tmchecker.git``


** Now you need to setup the URL, application ID and the API key of your Trend Micro Control Manager/Apex Central..**

* Open tmchecker.py and search for the following lines:

``
use_url_base = 'https://IP:443' # Trend Micro Control Manager/Apex Central server address
use_application_id = 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
use_api_key = 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx' # API key of Trend Micro CM/AC Server
``
* Change the value of use_url_base to the IP of your Control Manager/Apex Central
* For use_application_id and use_api_key you can obtain them by following these steps:
	* Go to `Administration > Settings > Automation API Access Settings`
	* In this page click on `add`, leave the checkbox enabled, then under `Application Access Settings`, define this script in the `Application name:` input box, ie, "tmchecker for checking agents health", copy Application ID and API key values from this page.
	* click `Save`

* Now go back to this script and paste the values of Application ID and API key you just copied inside the quotes of use_application_id and use_api_key respectively.


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

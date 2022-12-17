"""Run me to calibrate server configurations with respect to network adapter provided on command line.
"""

import subprocess
import argparse
import json
import sys
import os
import re

__home__ = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(__home__)))
from mytoolkit.txttag import TextTag as tag

if __name__ == "__main__":
    # import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("network", help="Network Adaptor Name")
    parser.add_argument("-p", "--port", help=f"Port to use, default is {None}", default=None)

    args = parser.parse_args()

    network = args.network
    port = args.port

    proc = subprocess.check_output("ipconfig").decode('utf-8')
    findings = re.findall(r'([\w\-\* ]*\w):[\w\-\*\:\.\s]+?IPv4 Address. . . . . . . . . . . : ([\d\.]*)', proc)

    IPMap = dict()

    for finding in findings:
        IPMap[finding[0]] = finding[1]

    config_file = open(__home__ + "config.json", "r")
    
    configuration = json.load(config_file)

    # configuration['serverIP'] = IPMap['Wireless LAN adapter Wi-Fi']
    try:
        configuration['serverIP'] = IPMap[network]
    
    except KeyError:
        print(f'{tag.error.b()}ERROR:{tag.error} Adapter not recognized{tag.close}')
        exit(1)

    if port is not None:
        configuration['vanilla port'] = int(port)
    
        config_file.close()
    
    config_file = open(__home__ + "config.json", "w")
    
    json.dump(configuration, config_file, indent=4)
    
    config_file.close()
    print(f"{tag.info.b()}Setup complete.{tag.info} Server configured with network {tag.id}{network}{tag.close}")

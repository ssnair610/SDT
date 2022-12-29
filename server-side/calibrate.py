"""Run me to calibrate server configurations with respect to network adapter provided on command line.
"""

import subprocess
import argparse
import json
import sys
import os
import re
import logging

__home__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__home__))

from mytoolkit.txttag import TextTag as tag

calib_logger = logging.getLogger("Server calibrate logger")
calib_logger.propagate = False
calib_logger.setLevel(logging.INFO)
if not calib_logger.handlers:
    fh = logging.FileHandler(filename='cshistory.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    fh.setFormatter(formatter)
    calib_logger.addHandler(fh)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("network", help="Network Adaptor Name")
    parser.add_argument("-p", "--port", help=f"Port to use, default is {None}", default=None)

    args = parser.parse_args()

    network = args.network
    port = args.port

    proc = subprocess.check_output("ipconfig").decode('utf-8')
    findings = re.findall(r'([\w\-\* ]*\w):(\s*.*\. :\s*)IPv4 Address. . . . . . . . . . . : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', proc)

    IPMap = dict()

    for finding in findings:
        IPMap[finding[0]] = finding[2]

    config_file = open(f"{__home__}/config.json", "r")
    
    configuration = json.load(config_file)

    # configuration['serverIP'] = IPMap['Wireless LAN adapter Wi-Fi']
    try:
        configuration['serverIP'] = IPMap[network]
        print(f'{tag.info}Found {tag.id}{network}{tag.info.b()} local IP Address.{tag.info} Processing...{tag.close}')
        calib_logger.info("IP address detected.")
    except KeyError as e:
        print(f'{tag.error.b()}ERROR:{tag.error} Adapter not recognized:{tag.id}{e}{tag.close}')
        calib_logger.error("Invalid Adaptor.")
        exit(1)

    if port is not None:
        configuration['vanilla port'] = int(port)
    
        config_file.close()
    
    config_file = open(f"{__home__}/config.json", "w")
    
    json.dump(configuration, config_file, indent=4)
    
    config_file.close()
    print(f"{tag.info.b()}Setup complete.{tag.info} Server configured with network {tag.id}{network}{tag.close}")
    calib_logger.info("Setup complete.")
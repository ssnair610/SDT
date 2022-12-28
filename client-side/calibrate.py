"""Run me to calibrate client configurations with respect to network adapter provided on command line.
"""

import subprocess
import argparse
import json
import sys
import os
import re

__home__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__home__))

from mytoolkit.txttag import TextTag as tag

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Catch network name and port address from command line
    parser.add_argument("network", help="Network Adaptor Name")
    parser.add_argument("serverIP", help="Server IP Address")
    parser.add_argument("-p", "--port", help=f"Port to use, default is {None}", default=None)

    
    # Gather network name and port address from parser
    args = parser.parse_args()

    network = args.network
    serverIP = args.serverIP
    port = args.port


    # Windows specific code: Catch Network names and their IPV4 addresses
    ipconfig_results = subprocess.check_output("ipconfig").decode('utf-8') 
    findings = re.findall(r'([\w\-\* ]*\w):(\s*.*\. :\s*)*IPv4 Address. . . . . . . . . . . : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ipconfig_results)


    # Map Network names to their IPV4 addresses
    IPMap = { finding[0] : finding[2] for finding in findings }


    try:
        # Prepare to set client configurations
        configuration = dict()

        try:
            # Setting serverIP to requested network
            configuration['clientIP'] = IPMap[network]
            print(f'{tag.info}Found {tag.id}{network}{tag.info.b()} network IP Address.{tag.info} Processing...{tag.close}')
        
        except KeyError as e:
            print(f'{tag.error.b()}ERROR:{tag.error} Adapter not recognized:{tag.id}{e}{tag.close}')
            print(f'{tag.info.b()}Adapters{tag.info} found on system:{tag.close}\r\n')

            for adapter in IPMap:
                print(f'{tag.id.b()}{adapter}{tag.close}')

            exit(1)

        
        # If port is specified, assign port address, else retain same port address as in configuration file
        if port is None:
            # Open configuration file to write into
            try:
                client_config_file = open(f"{__home__}/outbound/container/metadata.json", "r")
                
                configuration['receiverPort'] = json.load(client_config_file)['receiverPort']
                client_config_file.close()

            except KeyError as e:
                print(f'{tag.error.b()}ERROR:{tag.error} configuration file field missing:{tag.id}{e}{tag.close}')
                exit(1)
            
            except json.JSONDecodeError as e:
                print(f'{tag.error.b()}ERROR:{tag.error} json file decode failed:{tag.id}{e}{tag.close}')
                exit(1)

            except FileNotFoundError as e:
                print(f'{tag.error.b()}ERROR:{tag.error} configuration file not found:{tag.id}{e}{tag.close}')
                exit(1)

        else:
            configuration['vanilla port'] = int(port)

        # Overwrite configuration in configuration file
        client_config_file = open(f'{__home__}/outbound/container/metadata.json', 'w')
        
        json.dump(configuration, client_config_file, indent=4)
        client_config_file.close()

        server_config_file = open(f'{__home__}/metadata/config.json', 'w')
        json.dump({ 'serverIP': serverIP, "vanilla port" : 12000 }, server_config_file, indent=4)
        server_config_file.close()
    
    except FileNotFoundError as e:
        print(f'{tag.error.b()}ERROR:{tag.error} configuration file not found:{tag.id}{e}{tag.close}')
        exit(1)
    
    except json.JSONDecodeError as e:
        print(f'{tag.error.b()}ERROR:{tag.error} json file decode failed:{tag.id}{e}{tag.close}')
        exit(1)

    print(f"{tag.info.b()}Setup complete.{tag.info} Server configured with network {tag.id}{network}{tag.close}")
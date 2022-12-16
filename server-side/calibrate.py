import subprocess
import argparse
import json
import re

if __name__ == "__main__":
    # import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("network", help="Network Adaptor Name")
    parser.add_argument("-p", "--port", help=f"Port to use, default is {None}", default=None)

    args = parser.parse_args()

    network = args.network
    port = args.port

    proc = subprocess.check_output("ipconfig" ).decode('utf-8')
    findings = re.findall(r'([\w\-\* ]+):\r\s.*\s.*\s+IPv4 Address. . . . . . . . . . . : ([0-9.]*)', proc)

    IPMap = dict()

    for finding in findings:
        IPMap[finding[0]] = finding[1]

    config_file = open("config.json", "r")
    
    configuration = json.load(config_file)
    # configuration['serverIP'] = IPMap['Wireless LAN adapter Wi-Fi']
    try:
        configuration['serverIP'] = IPMap[network]
    
    except KeyError:
        print('Error: Adapter not recognized')
        exit(1)

    if port is not None:
        configuration['vanilla port'] = int(port)
    
        config_file.close()
    
    config_file = open("config.json", "w")
    
    json.dump(configuration, config_file, indent=4)
    
    config_file.close()
    print(f"Setup complete. Server configured with Network[{network}]")
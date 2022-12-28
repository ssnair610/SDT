import json
import os

__home__ = os.path.dirname(os.path.abspath(__file__))
__html__ = os.path.dirname(__home__) + "/templates/summary.html"
__sync__ = os.path.dirname(__home__) + "/sync.state"

def map_name(namefrom:str) -> str:
    if namefrom == 'client.E0':
        return 'Encryption 1 time'

    elif namefrom == 'client.E1':
        return 'Encryption 2 time'

    elif namefrom == 'client.H0':
        return 'Hashing time'

    elif namefrom == 'server.E0':
        return 'Decryption 1 time'

    elif namefrom == 'server.E1':
        return 'Decryption 2 time'

    elif namefrom == 'server.H0':
        return 'Rehashing time'
    
    return namefrom

if __name__ == '__main__':
    with open(f'{__home__}/analysis.json', 'r') as analysis_file:
        analysis = dict(json.load(analysis_file))

        tableData = dict()

        for party in ('client', 'server'):
            party_analysis = analysis[party]
            for process in party_analysis:
                tableData[map_name(party + "." + process) + " (s)"] = analysis[party][process]
        
        tableData['Throughput (MBps)'] = analysis['throughput'] * (2 ** -20)
        tableData['Transmit time (us)'] = analysis['transmit time'] * (10 ** 6)
        tableData['Archive size (bytes)'] = analysis['archive size']
        tableData['Encrypted archive size (bytes)'] = analysis['encrypted archive size']

        tablePretextHTML = str('<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"><title>Process Analysis</title></head><body><h1 style="margin-top: 50px; margin-left: 10px;">Results</h1>')
        
        tableHTML= str('<table class="table table-bordered" style="margin-top:100px; margin-left: 10px;"><thead><tr>')

        for heading in tableData.keys():
            tableHTML += '<th scope="col">' + heading + '</th>'
        
        tableHTML += '</tr></thead><tbody><tr>'

        for heading in tableData.keys():
            tableHTML += '<td>' + str(tableData[heading]) + '</td>'

        tableHTML += "</tr></tbody></table>"

        tablePosttextHTML = str("</body></html>")

        with open(__html__, 'w') as output_file:
            output_file.write(tablePretextHTML + tableHTML + tablePosttextHTML)
            output_file.flush()
    
    with open(__sync__, 'w') as sync_file:
        sync_file.write('1')
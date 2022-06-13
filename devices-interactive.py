import csv
from datetime import datetime
import time
import os
import meraki

# Either input your API key below by uncommenting line 10 and changing line 16 to api_key=API_KEY,
# or set an environment variable (preferred) to define your API key. The former is insecure and not recommended.
# For example, in Linux/macOS:  export MERAKI_DASHBOARD_API_KEY=093b24e85df15a3e66f1fc359f4c48493eaa1b73
# API_KEY = '093b24e85df15a3e66f1fc359f4c48493eaa1b73'

# DESCRIPTION:
# User selects OrgID & NetworkID to list devices at selected network, along with device ip/model/mac/serial-number.

def main():
    mStartTime = time.time()

    # Instantiate a Meraki dashboard API session
    dashboard = meraki.DashboardAPI(
        api_key='',
        base_url='https://api.meraki.com/api/v1/',
        output_log=False,
        log_file_prefix=os.path.basename(__file__)[:-3],
        log_path='',
        print_console=False
    )

    #### GET LIST OF ORGS FOR API KEY 
    organizations = dashboard.organizations.getOrganizations()
    orgTotal = len(organizations)


    # Display Orgs found with API-Key in use
    print(f'\nFound {orgTotal} Organizations with current API-Key:')
    dictOrg = {}
    counter = 1
    for org in organizations:
        orgID = org['id'].rstrip()
        orgName = org['name'].rstrip()
        dictOrg[str(counter)] = orgID
        print(f'#{counter} : {orgID:<3} : {orgName}')
        counter += 1

    #### USER INPUT - SELECT ORG
    inputOrg = input("-----------------\nMake a Selection: ")
    orgChoice = dictOrg[inputOrg]
    #print(f'{orgChoice}')

    try:
        # Get list of networks in organization
        networks = dashboard.organizations.getOrganizationNetworks(orgChoice)
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        print(f'status code = {e.status}')
        print(f'reason = {e.reason}')
        print(f'error = {e.message}')
    except Exception as e:
        print(f'some other error: {e}')

    total = len(networks)
    print(f'\n\n{total} networks found for orgID: {orgID}')

    #### GET NETWORK ID'S AND DEVICE COUNT PER NETWORK
    dictNet = {}
    counter = 1
    for net in networks:
        try:
            netID = net['id']
            netName = net['name']
            dictNet[str(counter)] = netID
            netDevices = dashboard.networks.getNetworkDevices(netID)
            totalDevices = len(netDevices)
            #print(f'#{counter:<4} : {netID:>20} : {netName:<50} : {totalDevices:>5} devices')
            print(f'#{counter:<4} : {netName:<50} : {totalDevices:>5} devices')
        except meraki.APIError as e:
            print(f'Meraki API error: {e}')
            print(f'status code = {e.status}')
            print(f'reason = {e.reason}')
            print(f'error = {e.message}')
        except Exception as e:
            print(f'some other error: {e}')
        counter += 1

    #USER INPUT - SELECT NET
    inputNet = input("-----------------\nMake a Selection: ")
    netIDchoice = dictNet[inputNet]
    #print(f'You Chose Network ID: {netIDchoice}')
    print(f'\nDevice list for network ID: {netIDchoice}\n-----------------\n')
    devices = dashboard.networks.getNetworkDevices(netIDchoice)
    for dev in devices:
        try:
            devName = dev['name']
            devLanIP = dev['lanIp']
            devMac = dev['mac']
            devSerial = dev['serial']
            devModel = dev['model']
            print(f'{devName:<35} : {devLanIP:<14} : {devModel:<10} : {devMac} : {devSerial:<10}')
        except Exception as e:
            print(f'error: {e}')





if __name__ == '__main__':
    startTime = time.time()
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\nKeyboardInterrupt Error: Stopped by User')
    endTime = time.time()
    runTime = round((endTime - startTime),2)
    print(f'\n----------------')
    print(f'Runtime {runTime} sec\n')



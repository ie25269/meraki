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
# List number of devices for each organization and network to which your API has access.

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

    # Get list of organizations to which API key has access
    organizations = dashboard.organizations.getOrganizations()
    orgTotal = len(organizations)

    # Display Orgs found with API-Key in use
    print(f'\nFound {orgTotal} Organizations with current API-Key:')
    for org in organizations:
        orgName = org['name'].rstrip()
        orgID = org['id'].rstrip()
        print(f' {orgID:<3} : {orgName}')

    # Iterate through list of orgs
    for org in organizations:
        org_id = org['id'].rstrip()
        org_name = org['name'].rstrip()
        try:
            # Get list of networks in organization
            networks = dashboard.organizations.getOrganizationNetworks(org_id)
        except meraki.APIError as e:
            print(f'Meraki API error: {e}')
            print(f'status code = {e.status}')
            print(f'reason = {e.reason}')
            print(f'error = {e.message}')
            continue
        except Exception as e:
            print(f'some other error: {e}')
            continue

        # Iterate through networks
        total = len(networks)
        counter = 1
        print(f'\n-----------------\n{org_id:<3} : {org_name} ({total} networks)')
        for net in networks:
            try:
                #Count Network Devices
                netID = net['id']
                netDevices = dashboard.networks.getNetworkDevices(netID)
                totalDevices = len(netDevices)
                #Show Network Names
                netName = net['name']
                print(f'  {netName:<50} : {netID:>20} : {totalDevices:>5} devices')
                #print(f'  {netName:<50} : {totalDevices:>5} devices')
            except meraki.APIError as e:
                print(f'Meraki API error: {e}')
                print(f'status code = {e.status}')
                print(f'reason = {e.reason}')
                print(f'error = {e.message}')
            except Exception as e:
                print(f'some other error: {e}')
            counter += 1


if __name__ == '__main__':
    startTime = time.time()
    main()
    endTime = time.time()
    runTime = round((endTime - startTime),2)
    print(f'\n----------------')
    print(f'Runtime {runTime} sec\n')



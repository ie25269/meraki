import csv
from datetime import datetime
import os
import time
import meraki

# Either input your API key below by uncommenting line 10 and changing line 16 to api_key=API_KEY,
# or set an env variable (preferred) to define your API key. The former is insecure and not recommended.
# For example, in Linux/macOS:  export MERAKI_DASHBOARD_API_KEY=myApiKey
# API_KEY = 'myApiKey'

# DESCRIPTION:
# List organization ID's associated to your API key.

def main():
    # Instantiate a Meraki dashboard API session
    dashboard = meraki.DashboardAPI(
        api_key='',
        base_url='https://api.meraki.com/api/v1/',
        output_log=False,
        log_file_prefix=os.path.basename(__file__)[:-3],
        log_path='',
        print_console=False
    )

    try:
        # Get list of organizations to which API key has access
        organizations = dashboard.organizations.getOrganizations()
        print(f'\nFound Organizations:')
        # Iterate through list of orgs
        for org in organizations:
            org_id = org['id'].rstrip()
            orgName = org['name'].rstrip()
            print(f' {orgName:<20}  ID: {org_id:<5}')
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        print(f'status code = {e.status}')
        print(f'reason = {e.reason}')
        print(f'error = {e.message}')
    except Exception as e:
        print(f'some other error: {e}')

if __name__ == '__main__':
    startTime = time.time()
    main()
    endTime = time.time()
    runTime = round((endTime - startTime),2)
    print(f'\n----------------')
    print(f'Runtime {runTime} sec\n')



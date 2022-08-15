import csv
import time
import os, sys, getopt
import meraki, json, pprint

# Set api key as ENV variable...  api_key=API_KEY
# DESCRIPTION:
# This script lists network names and ID's and takes one input (Org ID)

startTime = time.time()

#Parse args
argList = sys.argv[1:]
options = "ho:"
orgID = 'null'
netID = 'null'

if len(argList) < 1:
    print(f'\n----------\nError: must supply arguments -o <orgID> \n----------\n')
    sys.exit()
try:
    args, value = getopt.getopt(argList, options)
    for arg, val in args:
        if arg in ("-h"):
            printhelp()
            sys.exit()
        elif arg in ("-o"):
            orgID = val
except getopt.error as err:
    print("\nError: " , str(err) , "\n")
    sys.exit()

# Instantiate a Meraki dashboard API session
dashboard = meraki.DashboardAPI(
    api_key='',
    base_url='https://api.meraki.com/api/v1/',
    output_log=False,
    log_file_prefix=os.path.basename(__file__)[:-3],
    log_path='',
    print_console=False
)

print(f'-------------------------------\n')

networks = dashboard.organizations.getOrganizationNetworks(orgID)
for net in networks:
    try:
        netID = net['id']
        netName = net['name']
        print(f'{netName:<40} : {netID}')
    except Exception as e:
        print(f'error: {e}')




endTime = time.time()
runTime = round((endTime - startTime),2)
print(f'\n----------------')
print(f'OrgID: {orgID}')
print(f'Runtime {runTime} sec\n')




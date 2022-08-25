import csv
import time
import os, sys, getopt
import meraki, json, pprint
#
# DESCRIPTION:
#  This script lists network names and ID's and takes one input (Org ID)
#
# ENV variables used in this script:
#  MERAKI_DASHBOARD_API_KEY = <apiKey>    [REQUIRED]
#  MERAKI_ORG_SWITCHES = <switchesOrgID>  [OPTIONAL]
#  MERAKI_ORG_WIRELESS = <wirelessOrgID>  [OPTIONAL]

def printhelp():
    print( "\nDESCRIPTION:\n"
            " This script lists network names and network-ID's. It requires one input (Org ID)\n"
            "USAGE:\n" 
            " python3 <scriptName> -o <orgID>\n" 
            "ENV variables used in this script:\n" 
            " MERAKI_DASHBOARD_API_KEY = <apiKey>    [REQUIRED]\n" 
            " MERAKI_ORG_SWITCHES = <switchesOrgID>  [OPTIONAL]\n"
            " MERAKI_ORG_WIRELESS = <wirelessOrgID>  [OPTIONAL]\n\n")
    sys.exit()


startTime = time.time()

#Parse args
argList = sys.argv[1:]
options = "ho:"
orgID = 'null'

# ENV variables for easy org id switching.
env1 = "MERAKI_ORG_SWITCHES"
env2 = "MERAKI_ORG_WIRELESS"
if env1 in os.environ:
    orgIDswitches = os.environ.get(env1)
if env2 in os.environ:
    orgIDwireless = os.environ.get(env2)

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
            if val == "sw":
                orgID = orgIDswitches
            elif val == "wi":
                orgID = orgIDwireless
            else:
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
try:
    networks = dashboard.organizations.getOrganizationNetworks(orgID)
    for net in networks:
        netID = net['id']
        netName = net['name']
        print(f'{netName:<40} : {netID}')
except Exception as e:
    print(f'\n ERROR: {e}\n')
    sys.exit()

endTime = time.time()
runTime = round((endTime - startTime),2)
print(f'\n----------------')
print(f'OrgID: {orgID}')
print(f'Runtime {runTime} sec\n')


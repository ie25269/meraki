import csv
import time
import os, sys, getopt
import meraki, json, pprint
# Set/export ENV variable OR uncomment & change line below to manually enter api_key=API_KEY
# export MERAKI_DASHBOARD_API_KEY=yourAPIkeyGoesHere
# API_KEY = 'yourAPIkeyGoesHere'
startTime = time.time()

def printhelp():
    print(f'\nDESCRIPTION:\n This script displays clients found in the specified network')
    print(f'\nUSAGE:\n python3 <scriptName> -o <orgID> -n <netID> -s <searchTxt> -p <numPages>')
    print(f'\nARGS:\n -o[REQUIRED] -n[REQUIRED] -s[OPTIONAL] -p[OPTIONAL]')
    print(f'   -o <orgID>     : Organization ID to query')
    print(f'   -n <netID>     : Network ID to query')
    print(f'   -s <searchTxt> : Returns all clients with a groupPolicy8021x value matching your search text.') 
    print(f'   -s all         : Returns all clients with a non-empty value assigned to groupPolicy8021x.')
    print(f'   -p <numPages>  : Number of pages to request. Not Specified = ALL.\n\n')

orgIDswitches = ''
orgIDwireless = ''
orgID = 'null'
netID = 'null'
searchTxt = 'null'
pages = 'all'

# ENV variables for easy org id switching.
env1 = "MERAKI_ORG_SWITCHES"
env2 = "MERAKI_ORG_WIRELESS"
if env1 in os.environ:
    orgIDswitches = os.environ.get(env1)
if env2 in os.environ:
    orgIDwireless = os.environ.get(env2)

#Parse args
argList = sys.argv[1:]
options = "ho:n:s:p:"

if len(argList) < 4:
    print(f'\nError: must supply required arguments -o <orgID> -n <netID>\n')
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
        elif arg in ("-n"):
            netID = val
        elif arg in ("-s"):
            searchTxt = val
        elif arg in ("-p"):
            pages = val

except getopt.error as err:
    print("\nError: " , str(err) , "\n")
    print(f'        Required arguments -o <orgID> -n <netID>\n')
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

net = dashboard.networks.getNetwork(netID)
netName = net['name']
print(f'\n{netName:<45}  netID: {netID} ')
print(f'-------------------------------\n')

clientList = dashboard.networks.getNetworkClients(netID, total_pages=pages)
x = 1
for client in clientList:
    try:
        ipaddr = str(client['ip'])
        cID = str(client['id'])
        mac = str(client['mac'])
        gpolicy = str(client['groupPolicy8021x']).strip()
        status = str(client['status'])
        manuf = str(client['manufacturer'])
        devPort = str(client['switchport'])
        devVlan = str(client['vlan']).strip()
        devName = str(client['recentDeviceName']).strip()
        desc = str(client['description']).strip()
        if len(desc) > 14:
            desc = desc[0:14] + "..."
        if len(manuf) > 11:
            manuf = manuf[0:11] + "..."

        if searchTxt == 'null':
            print(f' {status:<8} {mac:<16} {ipaddr:<16} {desc:<18} {gpolicy:<14} {manuf:<14} vlan{devVlan:<4} {devName}/{devPort}')
            x += 1
        elif searchTxt == 'all' and gpolicy.lower() != 'none':
            print(f' {status:<8} {mac:<16} {ipaddr:<16} {desc:<18} {gpolicy:<14} {manuf:<14} vlan{devVlan:<4} {devName}/{devPort}')
            x += 1
        elif searchTxt != 'null' and gpolicy.lower() == searchTxt.lower():
            print(f' {status:<8} {mac:<16} {ipaddr:<16} {desc:<18} {gpolicy:<14} {manuf:<14} vlan{devVlan:<4} {devName}/{devPort}')
            x += 1

    except Exception as e:
        print(f'error: {e}')


numResults = str(x-1)
endTime = time.time()
runTime = round((endTime - startTime),2)
print(f'\n----------------')
print(f'Results: {numResults}')
print(f'OrgID: {orgID}')
print(f'{netName:<45} netID: {netID}')
print(f'Runtime {runTime} sec\n')




import csv
import time
import os, sys, getopt
import meraki, json, pprint
# Set/export ENV variable OR uncomment & change line below to manually enter api_key=API_KEY
# export MERAKI_DASHBOARD_API_KEY=yourAPIkeyGoesHere
# API_KEY = 'yourAPIkeyGoesHere'
startTime = time.time()

def printhelp():
    print(f'\nDESCRIPTION:\n This script displays all organizational clients matching group policy = searchText.')
    print(f'\nUSAGE:\n python3 <scriptName> -o <orgID> -s <searchTxt> -p <numPages>')
    print(f'\nARGS:\n -o[REQUIRED] -s[REQUIRED] -p[OPTIONAL]')
    print(f'   -o <orgID>     : Organization ID to query')
    print(f'   -s <searchTxt> : groupPolicy8021x search text.') 
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

if len(argList) < 3:
    printhelp()
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

print(f'-------------------------------\n')


# Grab network id's & names and store in dict
network = {}
try:
    netList = dashboard.organizations.getOrganizationNetworks(orgID)
    for net in netList:
        netID = net['id']
        netName = net['name']
        network[netID] = str(netName)
except Exception as e:
    print(f'\n ERROR: {e}\n')
    sys.exit()

# iterate through network id's and find matching clients

for netID in network:
    nname = network[netID]
    print(f'{nname:<40} :  {netID}')
    print(f'-----------------------------------')

    try:
        clientList = dashboard.networks.getNetworkClients(netID, total_pages=pages)
    except KeyboardInterrupt:
        numResults = str(x-1)
        endTime = time.time()
        runTime = round((endTime - startTime),2)
        print(f'\nERROR: stopped by User\n')
        print(f'\n----------------')
        print(f'Results: {numResults}')
        print(f'OrgID: {orgID}')
        print(f'Runtime {runTime} sec\n')
        sys.exit()
    except Exception as e:
        print(f'error: {e}')
        sys.exit()


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
    	    if searchTxt != 'null' and gpolicy.lower() == searchTxt.lower():
    	        print(f' {status:<8} {mac:<16} {ipaddr:<16} {desc:<18} {gpolicy:<14} {manuf:<14} vlan{devVlan:<4} {devName}/{devPort}')
    	        x += 1
        except KeyboardInterrupt:
            numResults = str(x-1) 
            endTime = time.time() 
            runTime = round((endTime - startTime),2)
            print(f'\nERROR: stopped by User\n')
            print(f'\n----------------') 
            print(f'Results: {numResults}')
            print(f'OrgID: {orgID}')
            print(f'Runtime {runTime} sec\n')
            sys.exit()
        except Exception as e:
    	    print(f'error: {e}')
    print(f'  ')


numResults = str(x-1)
endTime = time.time()
runTime = round((endTime - startTime),2)
print(f'\n----------------')
print(f'Results: {numResults}')
print(f'OrgID: {orgID}')
print(f'Runtime {runTime} sec\n')




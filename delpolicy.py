import csv
import time
import os, sys, getopt
import meraki, json, pprint

# Set api key as ENV variable  api_key=API_KEY
# DESCRIPTION:
#  Script deletes groupPolicy specified by NetworkID & PolicyID.

startTime = time.time()


#Parse args
argList = sys.argv[1:]
options = "hn:p:"
polID = 'null'
netID = 'null'

if len(argList) < 1:
    print(f'\n----------\nError: must supply arguments -n <networkID> -p <policyID>\n----------\n')
    sys.exit()
try:
    args, value = getopt.getopt(argList, options)
    for arg, val in args:
        if arg in ("-h"):
            printhelp()
            sys.exit()
        elif arg in ("-n"):
            netID = val
        elif arg in ("-p"):
            polID = val

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

print(f'-------------------------------')

try:
    sess = dashboard.networks.deleteNetworkGroupPolicy(netID,polID)
    print(f'Successfully deleted groupPolicyID {polID} from network {netID}')

except Exception as e:
    print(f'error: {e}')

endTime = time.time()
runTime = round((endTime - startTime),2)
print(f'\n----------------')
print(f'Runtime {runTime} sec\n')




import csv
import time
import os, sys, getopt
import meraki, json, pprint

# Set API key as an environment variable api_key=API_KEY
#
# DESCRIPTION:
#  This script copies group policy values from one network to another.
#  By default, only the firewallAndTrafficShaping object is copied.
# ARGUMENTS
#  -s <SourceNetworkID>  -d <DestinationNetworkID>  -p <PolicyID>
# REFERENCE:
#  https://developer.cisco.com/meraki/api/#!get-network-group-policies


startTime = time.time()

def printhelp():
    print(f'\nDESCRIPTION:\n This script copies a group policy (L3 Rules only) from one network to another')
    print(f'USAGE:\n python3 <script> -s <SourceNetworkID> -d <DestinationNetworkID> -p <PolicyID>')
    print(f'  <script> = Name of your python script\n  <SourceNetworkID> = NetworkID to copy from.')
    print(f'  <DestinationNetworkID> = NetworkID to copy to.\n  <PolicyID> = ID# of the policy to copy.\n')

#Parse args
argList = sys.argv[1:]
options = "hs:d:p:"
polID = 'null'
netID = 'null'

if len(argList) < 1:
    print(f'\n----------\nError: must supply arguments -s <srcNetworkID> -d <dstNetworkID> -p <srcPolicyID>\n----------\n')
    sys.exit()
try:
    args, value = getopt.getopt(argList, options)
    for arg, val in args:
        if arg in ("-h"):
            printhelp()
            sys.exit()
        elif arg in ("-s"):
            srcNetID = val
        elif arg in ("-d"):
            dstNetID = val
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

try:
    # Copy source network group policy and store into object 
    srcNet = dashboard.networks.getNetwork(srcNetID)
    srcNetName = srcNet['name']
    policy  = dashboard.networks.getNetworkGroupPolicy(srcNetID,polID)
    pName = policy['name']
    pRules = policy['firewallAndTrafficShaping']

    dstNet = dashboard.networks.getNetwork(dstNetID)
    dstNetName = dstNet['name']
 
    print(f'-------------------------------')
    print(f'\nCopying GroupPolicy {pName}(id#{polID}) from "{srcNetName}" to "{dstNetName}"...')
    # Copy new GroupPolicy into destination network
    sess = dashboard.networks.createNetworkGroupPolicy(dstNetID,pName,firewallAndTrafficShaping=pRules)
    newPolicyID = sess['groupPolicyId']
    newPolicyName = sess['name']
    print(f'Copy Successful to "{dstNetName}".\nCreated new policy {newPolicyID} - {newPolicyName}') 

except Exception as e:
    print(f'error: {e}')

endTime = time.time()
runTime = round((endTime - startTime),2)
print(f'\n----------------')
print(f'Runtime {runTime} sec\n')




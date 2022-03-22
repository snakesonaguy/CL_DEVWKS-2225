# Imported packages
import requests
import urllib3
import json
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

# Code specific requirements
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv(find_dotenv())

# Global variables accessed via python-dotenv
NSO_HOST = os.getenv('NSO_HOST')
USERNAME = os.getenv('NSO_USERNAME')
PASSWORD = os.getenv('NSO_PASSWORD')

# Additional global variables
AUTH = (USERNAME, PASSWORD)
VERIFY = False
HEADERS = {'Content-type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
DEVICES = []
PLATFORM_DETAILS = {}

## Verifies access to the RestConf API of NSO
def get_verify_restconf():
    path = '{}/restconf'.format(NSO_HOST)
    r = requests.get(path, auth=AUTH, headers=HEADERS, params=None, verify=VERIFY)
    if r.status_code == 200:
        ret = (json.loads(r.text))
        print(type(ret))
        # print(json.dumps(ret, indent=4))
    else:
        print('Error Code: {}'.format(r.status_code))

## Retrieves the device groups configured on NSO
def get_device_groups():
    ## You will need to edit the following line to gather only the members of the ALL group
    path = '{}/restconf/data/tailf-ncs:devices/device-group=ALL'.format(NSO_HOST)
    r = requests.get(path, auth=AUTH, headers=HEADERS, params=None, verify=False)
    if r.status_code == 200:
        ret = (json.loads(r.text))

        print(json.dumps(ret, indent=4))

        # UNCOMMENT 1 START
        groups = ret['tailf-ncs:device-group']
        for g in groups:
           print('Group Name: {}'.format(g['name']))
           print('\tMembers: ')
           for m in g['member']:
               print('\t\t{}'.format(m))
        # UNCOMMENT 1 STOP
        #
        # UNCOMMENT 2 START
               DEVICES.append(m)
        # UNCOMMENT 2 STOP
    else:
        print('Error Code: {}'.format(r.status_code))

def get_device_info():
    os = []
    version = []
    model = []
    serial = []

    for device in DEVICES:
        path = '{}/restconf/data/tailf-ncs:devices/device={}/platform'.format(NSO_HOST, device)
        r = requests.get(path, auth=AUTH, headers=HEADERS, params=None, verify=False)
        if r.status_code == 200:
            info = r.json()
            print(info)
            os.append(info['tailf-ncs:platform']['name'])
            version.append(info['tailf-ncs:platform']['version'])
            model.append(info['tailf-ncs:platform']['model'])
            serial.append(info['tailf-ncs:platform']['serial-number'])
        else:
            os.append('ERROR')
            version.append('ERROR')
            model.append('ERROR')
            serial.append('ERROR')

    data = {'OS Type': os, 'Version': version, 'Model': model, 'Serial': serial}

    df = pd.DataFrame(data, index=DEVICES)
    df.to_excel('test.xlsx')

    print(df)


def main():
    pass
    get_verify_restconf()
    # get_device_groups()
    # print(DEVICES)
    # get_device_info()


if __name__ == '__main__':
    main()
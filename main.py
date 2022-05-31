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
IP_DATA = []

## Verifies access to the RestConf API of NSO
def get_verify_restconf():
    path = '{}/restconf'.format(NSO_HOST)
    req = requests.get(path, auth=AUTH, headers=HEADERS, verify=VERIFY)
    if req.status_code == 200:
        data = req.json()
        print(json.dumps(data, indent=4))
    else:
        print('Error Code: {}'.format(req.status_code))

## Retrieves the device groups configured on NSO
def get_device_groups():
    ## You will need to edit the following line to gather only the members of the ALL group
    path = '{}/restconf/data/tailf-ncs:devices/device-group=ALL'.format(NSO_HOST)
    req = requests.get(path, auth=AUTH, headers=HEADERS, verify=False)
    if req.status_code == 200:
        data = (req.json())
        print(json.dumps(data, indent=4))

        # UNCOMMENT 1 START
        groups = data['tailf-ncs:device-group']
        for group in groups:
            print('Group Name: {}'.format(group['name']))
            print('\tMembers: ')
            for member in group['member']:
                print('\t\t{}'.format(member))
        # UNCOMMENT 1 STOP

        # UNCOMMENT 2 START
                DEVICES.append(member)
        # UNCOMMENT 2 STOP
    else:
        print('Error Code: {}'.format(req.status_code))

## Retrieves platform information for each individual device onboarded to NSO
def get_device_platform_details():
    os = []
    version = []
    model = []
    serial = []

    for device in DEVICES:
        path = '{}/restconf/data/tailf-ncs:devices/device={}/platform'.format(NSO_HOST, device)
        req = requests.get(path, auth=AUTH, headers=HEADERS, verify=False)
        if req.status_code == 200:
            data = req.json()
            os.append(data['tailf-ncs:platform']['name'])
            version.append(data['tailf-ncs:platform']['version'])
            model.append(data['tailf-ncs:platform']['model'])
            serial.append(data['tailf-ncs:platform']['serial-number'])
        else:
            error = 'Error Code: {}'.format(req.status_code)
            os.append(error)
            version.append(error)
            model.append(error)
            serial.append(error)

    PLATFORM_DETAILS['OS Type'] = os 
    PLATFORM_DETAILS['Version'] =  version 
    PLATFORM_DETAILS['Model'] = model 
    PLATFORM_DETAILS['Serial'] = serial

    # print(PLATFORM_DETAILS)

## Retrieves interface information for devices in DEVICES
def get_device_interfaces():

    os_mapping = {
        'ios-xe': 'ios',
        'ios-xr': 'ios-xr',
        'NX-OS': 'nx',
        'asa': 'asa',
    }

    for device in DEVICES:
        index = DEVICES.index(device)
        if 'Error Code:' not in PLATFORM_DETAILS['OS Type'][index]:
            os = (PLATFORM_DETAILS['OS Type'][index])
            call_mapping = os_mapping[os]
            ned_type = 'tailf-ned-cisco-{}:interface'.format(call_mapping)

            path = '{}/restconf/data/tailf-ncs:devices/device={}/config/{}'.format(NSO_HOST, device, ned_type)
            req = requests.get(path, auth=AUTH, headers=HEADERS, verify=False)
            
            if req.status_code == 200:
                data = req.json()
                format_ip_info(data, ned_type, device)
            else:
                print('Error Code: {}'.format(req.status_code))
        else:
            continue

def format_ip_info(data, ned, device):

    if ned == 'tailf-ned-cisco-ios:interface':
        interfaces = data[ned]
        for interface in interfaces.items():
            ports = interface[1]
            for port in ports:
                # print(ports)
                port_type = interface[0]
                port_number = port['name']
                port_ip_status = port['ip']
                # print(port_ip_status)

                if 'address' in port_ip_status:
                    address = port_ip_status['address']['primary']['address']
                    ip_data = (device, '{}{}'.format(port_type, port_number), address)
                    IP_DATA.append(ip_data)

    if ned == 'tailf-ned-cisco-nx:interface':
        interfaces = data[ned]
        for interface in interfaces.items():
            ports = interface[1]
            for port in ports:
                port_type = interface[0]
                port_number = port['name']

                if 'ip' in port:
                    port_ip_status = port['ip']
                    if 'address' in port_ip_status:
                        address = port_ip_status['address']['ipaddr']
                        ip_data = (device, '{}{}'.format(port_type, port_number), address)
                        IP_DATA.append(ip_data)

    if ned == 'tailf-ned-cisco-asa:interface':
        interfaces = data[ned]
        for interface in interfaces.items():
            ports = interface[1]
            for port in ports:
                port_type = interface[0]
                port_number = port['name']

                if 'ip' in port:
                    port_ip_status = port['ip']
                    if 'address' in port_ip_status:
                        address = port_ip_status['address']['ip']['host-ip']
                        ip_data = (device, '{}{}'.format(port_type, port_number), address)
                        IP_DATA.append(ip_data)

    if ned == 'tailf-ned-cisco-ios-xr:interface':
        interfaces = data[ned]
        for interface in interfaces.items():
            ports = interface[1]
            # print(interface)
            for port in ports:
                port_type = interface[0]
                port_number = port['id']

                if 'ipv4' in port:
                    port_ip_status = port['ipv4']
                    if 'address' in port_ip_status:
                        address = port_ip_status['address']['ip']
                        # print(port_ip_status)
                        # print(address)
                        ip_data = (device, '{}{}'.format(port_type, port_number), address)
                        # print(ip_data)
                        IP_DATA.append(ip_data)

## Creates a Pandas Data Frame 
def create_data_frame(data, index=None):
    df = pd.DataFrame(data, index=index)
    # Uncomment the line below if you want to see the formatting of the data frame.
    # print(df)
    return(df)

def main():
    pass
    get_verify_restconf()
    
    get_device_groups()
    
    get_device_platform_details()
    device_df = pd.DataFrame(PLATFORM_DETAILS, DEVICES)
    # device_df = create_data_frame(PLATFORM_DETAILS, DEVICES)
    device_df.to_excel('./inventory.xlsx')

    get_device_interfaces()
    ip_df = pd.DataFrame(IP_DATA, index=None)
    # ip_df = create_data_frame(IP_DATA)
    ip_df.to_excel('./ips.xlsx', index=False)
    


if __name__ == '__main__':
    main()
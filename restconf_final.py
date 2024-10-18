import json
from requests.auth import HTTPBasicAuth
import requests
import xmltodict
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.109/restconf/data/ietf-interfaces:interfaces"
loopback_name = 'Loopback65070171'
student_id = '65070171'

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Content-Type": "application/yang-data+json",
}
basicauth = HTTPBasicAuth("admin", "cisco")


def interface_exist():
    response = requests.get(f'{api_url}/interface={loopback_name}', auth=basicauth, verify=False)

    if response.status_code == 404:
        print("STATUS NOT FOUND: {}".format(response.status_code))

    return response.status_code != 404


def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.171.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }
    
    if interface_exist():
        return f"Cannot create: Interface loopback {student_id}"

    resp = requests.put(
        f'{api_url}/interface={loopback_name}', 
        data=json.dumps(yangConfig), 
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is created successfully"

    print('Error. Status Code: {} {}'.format(resp.status_code, resp.text))


def delete():
    if not interface_exist():
        return f"Cannot delete: Interface loopback {student_id}"

    resp = requests.delete(
        f'{api_url}/interface={loopback_name}', 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is deleted successfully"

    print('Error. Status Code: {}'.format(resp.status_code))


def enable():
    if not interface_exist():
        return f"Cannot enable: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.171.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        f'{api_url}/interface={loopback_name}',
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is enabled successfully"

    print('Error. Status Code: {}'.format(resp.status_code))


def disable():
    if not interface_exist():
        return f"Cannot shutdown: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.171.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        f'{api_url}/interface={loopback_name}',
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is shutdowned successfully"

    print('Error. Status Code: {}'.format(resp.status_code))
    return f"Cannot shutdown: Interface loopback {student_id}"


def status():
    if not interface_exist():
        return f"No Interface loopback {student_id}"

    api_url_status = f"{api_url}-state"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        payload = xmltodict.parse(resp.text)
        
        for intf in  payload.get('interfaces-state').get('interface'):
            if intf['name'] == loopback_name:
                interface = intf
    
        admin_status = interface['admin-status']
        oper_status = interface['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return f"Interface loopback {student_id} is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return f"Interface loopback {student_id} is disabled"
        
    print('Error. Status Code: {}'.format(resp.status_code))

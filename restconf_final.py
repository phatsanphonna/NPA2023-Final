import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.233/restconf/data/ietf-interfaces:interfaces"
loopback_name = 'loopback65070171'
student_id = '65070171'

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Content-Type": "application/yang-data+json",
}
basicauth = ("admin", "cisco")


def interface_exist():
    response = requests.get(f'{api_url}/interface={loopback_name}')
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

    print('Error. Status Code: {}'.format(resp.status_code))


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
    yangConfig = <!!!REPLACEME with YANG data!!!>

    resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
        <!!!REPLACEME with URL!!!>, 
        data=json.dumps(<!!!REPLACEME with yangConfig!!!>), 
        auth=basicauth, 
        headers=<!!!REPLACEME with HTTP Header!!!>, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "<!!!REPLACEME with proper message!!!>"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def disable():
    yangConfig = <!!!REPLACEME with YANG data!!!>

    resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
        <!!!REPLACEME with URL!!!>, 
        data=json.dumps(<!!!REPLACEME with yangConfig!!!>), 
        auth=basicauth, 
        headers=<!!!REPLACEME with HTTP Header!!!>, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "<!!!REPLACEME with proper message!!!>"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def status():
    api_url_status = "<!!!REPLACEME with URL of RESTCONF Operational API!!!>"

    resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
        <!!!REPLACEME with URL!!!>, 
        auth=basicauth, 
        headers=<!!!REPLACEME with HTTP Header!!!>, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = <!!!REPLACEME!!!>
        oper_status = <!!!REPLACEME!!!>
        if admin_status == 'up' and oper_status == 'up':
            return "<!!!REPLACEME with proper message!!!>"
        elif admin_status == 'down' and oper_status == 'down':
            return "<!!!REPLACEME with proper message!!!>"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "<!!!REPLACEME with proper message!!!>"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))

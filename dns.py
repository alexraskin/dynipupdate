import json
import requests

#get ip of localhost
ip = str(requests.get('http://icanhazip.com').text.rstrip())

fqdn = '<FDQN HERE>'
#FQDN in DYN

s = requests.Session()
session_url = 'https://api.dynect.net/REST/Session/ARecord'
s.headers.update({"Content-Type": "application/json"})
auth_info = json.dumps({"password": "<PASSWORD>", "user_name": "<USERNAME>", "customer_name": "<CUSTOMERNAME>"}, indent=4)
auth_response = json.loads(s.post(session_url, data=auth_info).text)
s.headers.update({"Auth-Token": "%s" % auth_response['data']['token']})
api_url = 'https://api.dynect.net'
recordnumber = s.get(api_url + '/REST/ARecord/<DOMAINNAME>/%s' % fqdn).json()
print recordnumber
arecord = s.get(api_url + recordnumber['data'][0]).json()['data']['rdata']['address']
print arecord
payload = json.dumps({"rdata": {"address": "%s" % ip}}, indent=4)

if not ip == arecord:
    headers = {'Content-type': 'application/json',}
    data = '{"text": "%s IP changed to %s"}' % (fqdn, ip)
    response = requests.post('<SLACK WEBHOOK URL>', headers=headers, data=data)
else:
    print ("IP is the same")


print json.dumps(arecord, indent=4)
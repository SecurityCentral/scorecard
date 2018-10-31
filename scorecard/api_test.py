import requests


capability = requests.get('http://scorecard.int.open.paas.redhat.com/securitycapabilities/?search=fips').json()
print(capability[0]['id'])

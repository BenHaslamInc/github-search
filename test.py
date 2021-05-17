#!/usr/bin/env python

import requests

# response = requests.head('https://api.github.com/repos/clearmatics/autonity/license')
org = 'BenHaslamInc'
repo = 'python-chess2'
url = 'https://api.github.com/repos/' + org + '/' + repo + '/license'
github_token = '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'

headers = {
    'Accept': 'application/vnd.github.v3+json',
    "Authorization": "Bearer " + github_token,
    'Branch': 'edit'

}


response = requests.head(url,headers=headers)
print (response)

if str(response) == '<Response [200]>':
    print ('we got em')

# print (response)
# if response == 200:
#     print ('we got em good')
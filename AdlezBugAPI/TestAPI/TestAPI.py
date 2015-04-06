#This tests the instance of the API on the Adlez website.
#Copyright (c) 2015 Milkey Mouse

import webbrowser
#import requests
import urllib2
import json
import sys

head = sys.argv[1]
body = sys.argv[2]

test_json = {"title" : head, "body" : body}

test_json = json.dumps(test_json)
headers = {"Content-Type":"application/json"}
req = urllib2.Request("http://team-ivan.com:1337/report", test_json, headers)
result_json = json.loads(urllib2.urlopen(req).read())

#r = requests.post("http://team-ivan.com:1337/report", data=test_json, headers=headers)
#result_json = r.json()

print result_json["url"]

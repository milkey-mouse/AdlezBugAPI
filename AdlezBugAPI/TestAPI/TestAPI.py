#This tests the instance of the API on the Adlez website.
#Copyright (c) 2015 Milkey Mouse

import webbrowser
import requests
import pprint
import json

head = raw_input("Title: ")
body = raw_input("Description: ")

print "Requesting..."

test_json = {"title" : head, "body" : body}

headers = {"Content-Type":"application/json"}

r = requests.post("http://team-ivan.com:1337/report", json=test_json, headers=headers)

result_json = r.json()

pprint.PrettyPrinter().pprint(result_json)

print "Topic created at " + result_json["url"]

webbrowser.open(result_json["url"])

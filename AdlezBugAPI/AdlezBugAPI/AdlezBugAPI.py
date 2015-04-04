#Copyright (c) 2015 Milkey Mouse

from flask import Flask, request, jsonify, abort, make_response
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/report", methods=["POST"])
def report():
    if not request.json:
        #it wasn't json
        abort(400)
    try:
        title = request.json["title"]
        body = request.json["body"]
        if len(title) > 80:
            abort(400)
        print "Bug submitted: \"" + title + "\""
        print "Body: " + body
    except:
        #there weren't the required fields in the json
        abort(400)
    url = send_to_server(title, body)
    return jsonify({"url":url})
    
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'The server derped'}), 500)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

def send_to_server(title, body):
    print "Getting nonce..."
    form = {}
    wpt = requests.get("http://team-ivan.com/blog/forums/forum/bug-reports/")
    orig_webpage = BeautifulSoup(wpt.text)
    for input in orig_webpage.find_all("input"):
        if not input.get("id") == "_wpnonce":
            continue
        try:
            print input.get("id") + " : " + input.get("value")
            form[input.get("id")] = input.get("value")
        except:
            pass
    print "Got nonce: " + form["_wpnonce"]
    print "Forming request..."
    form["bbp_anonymous_name"] = "Adlez Bug Submitter"
    form["bbp_anonymous_website"] = "http://team-ivan.com/"
    form["bbp_anonymous_email"] = "milkeymouse@team-ivan.com"
    form["bbp_topic_title"] = title
    form["bbp_topic_content"] = body
    form["bbp_topic_submit"] = ""
    form["bbp_forum_id"] = "137"
    form["action"] = "bbp-new-topic"
    form["_wp_http_referer"] = "/blog/forums/forum/bug-reports/"
    print "Requesting..."
    r = requests.post("http://team-ivan.com/blog/forums/forum/bug-reports/", data=form) #http://httpbin.org/post
    print "Request successful!"
    loc = r.url
    print "Topic created at " + loc
    return loc

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0",port=1337)
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

import requests, re, ast

def userId(f_username):

    x = requests.get("https://www.facebook.com/" + f_username)

    matchs = re.findall(r'\"userID\":\"[0-9]+\"', x.text)
    ids = []
    for match in matchs:
        match = "{" + match + "}"
        match_as_dict = ast.literal_eval(match)
        ids.append(match_as_dict["userID"])

    if len(ids) > 0:
        return ids[0]
    
    return "ERROR: id not found"

@app.route('/fid', methods=['GET'])
def home():
    if 'username' in request.args:
        return jsonify(userId(request.args['username']))
    else:
        return jsonify("Error: No username field provided. Please specify an username.")

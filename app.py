import flask
import requests, re, ast
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


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


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/fid', methods=['GET'])
def getFacebookID():
    if 'username' in request.args:
        return jsonify(userId(request.args['username']))
    else:
        return jsonify("Error: No username field provided. Please specify an username.")

@app.route('/ig', methods=['GET'])
def getCode():
    if 'code' in request.args:
        return jsonify(request.args['code'])
    else:
        return jsonify("Error: No code field provided.")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


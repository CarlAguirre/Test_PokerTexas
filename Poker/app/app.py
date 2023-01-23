from flask import Flask, jsonify, request
import json

app= Flask(__name__)

@app.route("/poker/validation", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running poker/validation ...!!!!"
    return jsonify(json)

@app.route("/poker/validation", methods=['POST'])
def manos():

    manos_New={
    "hand1": request.json['hand1'],
    "hand2": request.json['hand2']
    }
    
    return 'received'


if __name__ == '__main__':
    app.run (debug=True, port=9999)
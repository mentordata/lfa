import socket
import sys
import requests
from typing import final
from email import message_from_string
import re
import json
import pandas as pd
import datetime
import webbrowser
# SPECIFYING HOST AND PORT
HOST = ''
PORT = 5000

soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

try:
    soc.bind((HOST,PORT))
except socket.error as message:
    print('Bind failed. Error Code: '
        + str(message[0]) + ' Message '
        + message[1])
    sys.exit()

soc.listen(1)
print("Opening site...")
webbrowser.open('LIVE LOGONVALIDATION SITE')
# LISTENING TO LOG IN PROCESS AND REQUESTING AUTHORIZATION CODE

while True:
    print('waiting for a connection')
    conn, address = soc.accept()

    try:
        print('Connection from ',address)

        while True:
            data = conn.recv(4096)
            #print('received "%s"' % data)
            response = data.decode("utf-8")
            m = re.search('code=(.+?)&state',response)
            if m:
                found = m.group(1)
                print("FOUND AUTH CODE: "+found)
                break
            if not data:
                break
    finally:
        conn.close()
        break

# REQUESTING TOKEN
headers = {
    'Content-type': 'application/x-www-form-urlencoded',
}

data = {
  'grant_type': 'authorization_code',
  'code':found,
  'redirect_uri': 'URL FOR REDIRECT',
  'client_id': 'APP_KEY',
  'client_secret': 'APP_SECRET'
}

response = requests.post('https://live.logonvalidation.net/token', headers=headers, data=data, verify=False)
print(response.content)

x = response.content.decode("utf-8")
y = re.search('access_token":"(.+?)","',x)
token = y.group(1)
print(token)

# DOWNLOADING DATA
headers = {
    'Authorization': 'Bearer %s' % (token),
    'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.get('https://gateway.saxobank.com/openapi/port/v1/positions/', headers=headers, verify=False)
json_data = json.loads(response.text)
print(json.dumps(json_data,indent=4))

# SAVING DATA TO CSV FILE
df = pd.json_normalize(json_data['Data'])
filename = "SAXO_POS_"+datetime.datetime.today().strftime(':%Y_%m_%d') + ".csv"
df.to_csv(filename,header=True,index=None)

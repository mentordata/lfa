import socket
import sys
import requests
from sys import argv
import re
import json
import pandas as pd
import datetime
import webbrowser
import paramiko
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
webbrowser.open('https://live.logonvalidation.net:443/login/?requestId=NDQ0Y2EwMzIwNjk3NDJiNTk2ZDUyMmI3NmY4OGE1ZmUyOTI2MTg1&mode=oauth')
# LISTENING TO LOG IN PROCESS AND REQUESTING AUTHORIZATION CODE

while True:
    print('waiting for a connection')
    conn, address = soc.accept()

    try:
        print('Connection from ',address)

        while True:
            data = conn.recv(4096)
            #print('received "%s"' % data)  # uncomment if you want to see what is received
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

#print("#2 CODE:_",found)

# REQUESTING TOKEN
headers = {
    'Content-type': 'application/x-www-form-urlencoded',
}

data = {
  'grant_type': 'authorization_code',
  'code':found,
  'redirect_uri': 'http://localhost:5000/liveapp',
  'client_id': 'APP KEY',
  'client_secret': 'APP SECRET'
}

response = requests.post('https://live.logonvalidation.net/token', headers=headers, data=data, verify=False)
#print(response.content)

x = response.content.decode("utf-8")
y = re.search('access_token":"(.+?)","',x)
token = y.group(1)
print(token)

# DOWNLOADING DATA
headers = {
    'Authorization': 'Bearer %s' % (token),
    'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.get('https://gateway.saxobank.com/openapi/port/v1/positions/?FieldGroups=greeks,exchangeinfo,positionbase,positionview&ClientKey=x9RQ1PMdoLmK|X8oij-MGw==', headers=headers, verify=False)
json_data = json.loads(response.text)
print(json.dumps(json_data,indent=4))

# SAVING DATA TO CSV FILE
df = pd.json_normalize(json_data['Data'])
filename = "SAXO_POS_"+datetime.datetime.today().strftime('%Y_%m_%d') + ".csv"
df.to_csv(filename,header=True,index=None)
print("New file"+filename+" has been created.")

# CREATING SSH TUNNEL TO SEND FILE
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname="dev.mentordata.com",username=argv[1],password=argv[2])

target = "/home/lfa/saxo/dane/"+filename
ftp_client = ssh_client.open_sftp()
ftp_client.put(filename,target)
print("Ssh connection created. File ["+filename+"] has been uploaded.")
ftp_client.close()



stdin,stdout,stderr=ssh_client.exec_command("ls /home/lfa/saxo/dane")
for i in stdout:
    print(i)



ssh_client.close()

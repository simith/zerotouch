import requests
import json
import uuid

def storeFile(fileContents,fileName):
    with open(fileName, "w") as myfile:
        myfile.write(fileContents)
        myfile.close()


def getCerts():
    thingName = str(uuid.uuid4())
    r = requests.get('http://127.0.0.1:5000/ztouch/thing/'+thingName+'/certs/')
    print(r.text)
    if r.status_code == 200:
        j = json.loads(r.text)
        print(j['thing'])
        storeFile(j['device-cert'],thingName+"-test.crt")
        storeFile(j['device-privkey'],thingName+"-privkey-test.key")
        #rootca-cert
        storeFile(j['rootca-cert'],thingName+"-rootca-cert-test.crt")

if __name__ == "__main__":
    getCerts()
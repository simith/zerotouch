from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import requests
import json
import uuid

from certmaker.certgen import CertGenerator

thingName=""

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")


def getThingName():
    return str(uuid.uuid4())

def bootstrapThing():
    #check whether we have certs required to start, assume we have a thing name
    #get thing name
    global thingName
    thingName = getThingName()
    print("Thing name:"+thingName)
    #get the Provisioning server IP, send a broadcast packet out


def connectToAwsIot():
  
    #host = "a1bb7j6i5uiivh.iot.us-east-1.amazonaws.com"
    host = "a1bb7j6i5uiivh.iot.ap-southeast-2.amazonaws.com"
    rootCAPath = "iotRootCA.pem"
    certificatePath = thingName+"-test.crt"
    privateKeyPath = thingName+"-privkey-test.key"  
    clientId = thingName
    topic = "foo/bar/something"
    print("Root CA Path = " +certificatePath )

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    #Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host,8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    #myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    #myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    #myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    #myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    print("Subscribing to topic:"+topic);
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(2)

    # Publish to the same topic in a loop forever
    loopCount = 0
    while True:
        print("PUBLISH being sent now:" + "New Message " )
        myAWSIoTMQTTClient.publish(topic, "New Message " + str(loopCount), 1)
        loopCount += 1
        time.sleep(10)



def storeFile(fileContents,fileName):
    with open(fileName, "w") as myfile:
        myfile.write(fileContents)
        myfile.close()


def getCerts():
    global thingName
    r = requests.get('http://127.0.0.1:5000/ztouch/thing/'+thingName+'/certs/')
    print(r.text)
    if r.status_code == 200:
        j = json.loads(r.text)
        print(j['thing'])
        storeFile(j['device-cert'],thingName+"-test.crt")
        storeFile(j['device-privkey'],thingName+"-privkey-test.key")
        #rootca-cert
        storeFile(j['rootca-cert'],thingName+"-rootca-cert-test.crt")


def init():
    #call create certs, if certs not present
    bootstrapThing()
    getCerts()
    connectToAwsIot()

if __name__ == '__main__':
    init()
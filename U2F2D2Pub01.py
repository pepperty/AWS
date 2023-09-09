'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''
 # PJ:XT PYT_BPU_Tank

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json

# Sub process
import subprocess
import platform

# Stop Node-RED
if platform.system() == "Windows":
    node_red_path = r'C:\Users\peppe\AppData\Roaming\npm\node-red.cmd'
    subprocess.call(['taskkill', '/F', '/IM', 'node-red'])
    subprocess.Popen([node_red_path])
if platform.system() == "Linux":
    subprocess.call(['killall', 'node-red'])
    subprocess.Popen(['node-red'])

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# host = "aquiml1rupuga-ats.iot.ap-southeast-1.amazonaws.com"
# rootCAPath = "certs/AmazonRootCA1.pem"
# certificatePath = "certs/device.pem.crt"
# privateKeyPath = "certs/private.pem.key"

host = "a1x0dm3q26289z-ats.iot.ap-southeast-1.amazonaws.com"
rootCAPath = "certsP/AmazonRootCA1.pem"
certificatePath = "certsP/device.pem.crt"
privateKeyPath = "certsP/private.pem.key"

port = 8883
useWebsocket = False
clientId = "LIV24"
topic = "iot/boosterpump"

if not useWebsocket and (not certificatePath or not privateKeyPath):
    print("Missing credentials for authentication.")
    exit(2)

# Port defaults
if useWebsocket and not port:  # When no port override for WebSocket, default to 443
    port = 443
if not useWebsocket and not port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
mode = 'publish'
myAWSIoTMQTTClient.connect()
if mode == 'both' or mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
# Read data from JSON file
with open('BPU_2L31.json', 'r') as file:
    json_data1 = json.load(file)
# print(json_data)
while True:
    if mode == 'both' or mode == 'publish':
        messageJson1 = json.dumps(json_data1)
        myAWSIoTMQTTClient.publish(topic, messageJson1, 1)
        # if mode == 'publish':
        #     print('Published topic %s: %s\n' % (topic, messageJson))
    time.sleep(30)

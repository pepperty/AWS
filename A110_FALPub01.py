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

#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import logging
import time
import json

# Sub process
import subprocess
import platform

# Pi IO
import RPi.GPIO as GPIO
# Define GPIO to use on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IO_05_AL = 5 
IO_13_TB = 13

GPIO.setup(IO_05_AL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_13_TB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Stop Node-RED
# if platform.system() == "Windows":
#     node_red_path = r'C:\Users\peppe\AppData\Roaming\npm\node-red.cmd'
#     subprocess.call(['taskkill', '/F', '/IM', 'node-red'])
#     subprocess.Popen([node_red_path])
# if platform.system() == "Linux":
#     subprocess.call(['killall', 'node-red'])
#     subprocess.Popen(['node-red'])

# Configure AWS IoT endpoint
iot_client = boto3.client('LIV24', region_name='ap-southeast-1')

# Path to your device's certificates
root_ca_path = 'certsP/AmazonRootCA1.pem'
private_key_path = 'certsP/private.pem.key'
certificate_path = 'certsP/device.pem.crt'

# Connect to AWS IoT
iot_client.create_keys_and_certificate(setAsActive=True)
iot_client.attach_principal_policy(
    policyName='Liv24Policy',
    principal=iot_client.describe_endpoint()['a1x0dm3q26289z-ats.iot.ap-southeast-1.amazonaws.com']
)

with open('AWS\A110_FAL.json', 'r') as file:
    json_data1 = json.load(file)
# print(json_data)
if __name__ == '__main__':
    try:
        while True:
            # print("################")
            # print(json_data1['devices'][0]['tags'][2])
            # print("################")
            if GPIO.input(IO_05_AL) == 0:
                json_data1['devices'][0]['tags'][2]['value']="Z1_DZ_1_FL1_LOBBY"
            else:
                json_data1['devices'][0]['tags'][2]['value']=""
            if GPIO.input(IO_13_TB) == 0:
                json_data1['devices'][0]['tags'][3]['value']="Trouble"
            else: 
                json_data1['devices'][0]['tags'][3]['value']=""
            # messageJson1['devices']['tags']['value'] = str(35.00)
            # Publish data to a specific AWS IoT topic
            iot_client.publish(
                topic='iot/firealarm',
                qos=1,
                payload=json.dumps(json_data1)
            )
            time.sleep(30)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    except Exception as e:
        print(f"An error occurred: {e}")
        GPIO.cleanup()
    GPIO.cleanup()

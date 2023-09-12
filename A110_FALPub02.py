import boto3
import json
import time

# Pi IO
import RPi.GPIO as GPIO
# Define GPIO to use on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IO_05_AL = 5 
IO_13_TB = 13

GPIO.setup(IO_05_AL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IO_13_TB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

while True:
    # Your data collection logic here
    data = {
        'temperature': 25.5,
        'humidity': 60.2
    }

    # Publish data to a specific AWS IoT topic
    iot_client.publish(
        topic='your-topic-name',
        qos=1,
        payload=json.dumps(data)
    )

    time.sleep(5)  # Adjust the interval as needed

#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt
import ssl
import json

# Callback function when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT with result code: " + str(rc))
    # Subscribe to the desired topic
    client.subscribe("raspi/data")  # Replace 'raspi/data' with your topic if different

# Callback function when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Message received from topic {msg.topic}: {msg.payload.decode('utf-8')}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Configure TLS/SSL settings
client.tls_set(ca_certs='./DEVICE_Certificates/rootCA.pem', 
               certfile='./DEVICE_Certificates/certificate.pem.crt', 
               keyfile='./DEVICE_Certificates/private.pem.key', 
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)

# Connect to AWS IoT Core
client.connect("a3cz6591mmwk24-ats.iot.ap-south-1.amazonaws.com", 8883, 60)

# Start the MQTT client loop to listen for incoming messages
client.loop_forever()


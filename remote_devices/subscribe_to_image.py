import paho.mqtt.client as mqtt

import random
import time
import datetime
from datetime import datetime, timedelta

import os

import sched

import json

import binascii


#broker = '127.0.0.1'
broker = '192.168.1.245'
#broker = 'mqtt://mosquitto'
port = 1883
topic = [("camera_101/picture",0),("camera_102/picture",0)]
client_id = f'python-mqtt-1337'
username = 'andy'
password = 'cannondale'
camera_picture_delay = 20

global image
global new_file_name

new_file_name = False
image = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def subscribe(client):
    def on_message(client, userdata, message):

        #print(message.payload)
        if message.payload == "file_name01":
            print("found 101")
        if message.payload == "file_name02":
            print("found 102")

        if "file_name02" in str(message.payload):
            #print(message.payload.decode())
            msg = json.loads(message.payload.decode())
            #res=json.loads(str(msg))
            #print(str(msg["file_name"]))
            new_file_name = str(msg["file_name02"])

            #print(new_file_name)

            ba = binascii.a2b_base64((msg["picture"]))
            f = open(new_file_name, 'wb')
            f.write(ba)
            f.close()

        if "file_name01" in str(message.payload):
            #print(message.payload.decode())
            msg = json.loads(message.payload.decode())
            #res=json.loads(str(msg))
            #print(str(msg["file_name"]))
            new_file_name = str(msg["file_name01"])

            #print(new_file_name)

            ba = binascii.a2b_base64((msg["picture"]))
            f = open(new_file_name, 'wb')
            f.write(ba)
            f.close()
        
        #with open(incoming_message) as infile:
        #    data = json.load(infile)

        #decoded_message = json.load(incoming_message)
        #res = json.loads(str(msg))
        #print(msg)


    '''def on_message_file_name(client, userdata, msg):        
        new_file_name = str(msg.payload)
        print("file name: " + new_file_name)

    def save_image():
        while image == False or new_file_name == False:
            time.sleep(0.001)
        f = open(new_file_name, 'wb')
        f.write(image)
        f.close()
           

    def on_message_picture(client, userdata, msg):
        image=msg.payload  
        print ('image received')
    '''

    client.subscribe(topic)
    client.on_message = on_message



scheduled_time = sched.scheduler(time.localtime, time.sleep)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
#mqttc.on_message = on_message
mqttc.username_pw_set(username, password)
mqttc.connect(broker, port, 60)

subscribe(mqttc)
mqttc.loop_forever()

#configure_camera(scheduled_time, mqttc)
#publish2(mqttc)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#mqttc.loop_forever()
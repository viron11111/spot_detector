import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import random
import time
import datetime
from datetime import datetime, timedelta

import os

from picamera2 import Picamera2, Preview
from libcamera import controls

import binascii

import sched

import json


#broker = '127.0.0.1'
broker = '192.168.1.245'
#broker = 'mqtt://mosquitto'
port = 1883
topic = "camera_102/picture"
client_id = f'right_camera_102'
username = 'andy'
password = 'cannondale'
camera_picture_delay = 10
size = (4608, 2592) #(2304, 1296) #(640,480)   #(4608, 2592)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))

def configure_camera(scheduled_time, mqttc):
    picam2 = Picamera2()
        
    camera_config = picam2.create_still_configuration(main={"size": size}, lores={"size": (320, 240)}, display="lores")
    picam2.configure(camera_config)
    picam2.set_controls({"AfMode":controls.AfModeEnum.Continuous})
    #picam2.set_controls({"AfMode":controls.AfModeEnum.Manual, "LensPosition": 10.0})
    #picam2.set_controls({"AfRange":controls.AfModeEnum.Continuous})
    #picam2.start_preview(Preview.QTGL)
    picam2.start()

    time_now = roundTime()
    time_future = time_now + timedelta(seconds=camera_picture_delay)
    #print("time_now: " + str(time_now) + " time_future: " + str(time_future))
    #time.sleep(10)
    
    num_o_pics = 0
    #print(datetime.now())
    while True:
        while True:
            if datetime.now() > time_future:
                break
        take_picture(picam2, mqttc)

        print("time_now: " + str(time_now) + " time_future: " + str(time_future))

        time_now = roundTime()
        time_future = time_now + timedelta(seconds=camera_picture_delay)

        #num_o_pics= num_o_pics+1    


def take_picture(picam2, mqttc):    
    #print("here")
    #time.sleep(2)
    file_time = str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))
    #print("here1")
    #time.sleep(2)
    file_name = "camera_102_" + file_time + ".jpg"
    #print("here2")
    #time.sleep(2)
    picam2.capture_file("/home/andy/software/pictures/" + file_name)

    #ram_image = picam2.capture_array()

    #print("here3")
    #time.sleep(2)

    list_of_files = os.listdir('/home/andy/software/pictures/')
    #print("here4")
    #time.sleep(5)
    full_path = ["/home/andy/software/pictures/{0}".format(x) for x in list_of_files]

    with open("/home/andy/software/pictures/" + file_name,'rb') as file:    
        #filecontent = file.read()
        #byteArr = bytearray(filecontent)

        image_data = binascii.b2a_base64(file.read()).decode()
        #image_data = binascii.b2a_base64(ram_image).decode()
    #image_data = binascii.b2a_base64(ram_image).decode()

        pic_payload = json.dumps({"file_name02":file_name, "picture":image_data})
    #pic_payload = json.dumps({"file_name02":file_name, "picture":image_data})

    publish.single("camera_102/picture", payload=pic_payload, qos=2, hostname='192.168.1.245', port=1883, auth = {'username':"andy", 'password':"cannondale"})

    #publish(mqttc, file_name)
    #publish2(mqttc)

    while len(list_of_files) > 20:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)
        list_of_files = os.listdir('/home/andy/software/pictures/')
        full_path = ["/home/andy/software/pictures/{0}".format(x) for x in list_of_files]

'''def publish(client, file_name):
    #client.publish('camera_101/file_name', file_name)
    

        #pic_payload = json.dumps({"picture":image_data})

    #result = client.publish(topic,pic_payload)

    


    #result = client.publish(topic,byteArr,2)
    msg_status = result[0]
    if msg_status == 0:
        print(f"message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")'''



def roundTime(dt=None, dateDelta=timedelta(seconds=camera_picture_delay)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dt == None : dt = datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds,-dt.microsecond)

def publish2(client):
    #topic = "python/mqtt"
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 1:
            break

#print("sleeping for 10")
#time.sleep(10)

scheduled_time = sched.scheduler(time.localtime, time.sleep)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
#mqttc.on_message = on_message
mqttc.username_pw_set(username, password)
mqttc.connect(broker, port, 60)

configure_camera(scheduled_time, mqttc)
publish2(mqttc)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#mqttc.loop_forever()
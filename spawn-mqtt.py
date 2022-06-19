# MQTT MULTI LEVEL DEVICE EMULATOR FOR EDGEX
# spawns an emulated mqtt device with multithreading
# responds and generates async events
# 
## USAGE : spawn-mqtt-ml.py <device_name> <response>

# UTILS FOR DEBUGGING
# listen on topic: mosquitto_sub -d -h <host> -t <topic>
# listen on all: mosquitto_sub -d -h <host> -t "#"

#from random import seed
#from random import randint
import paho.mqtt.client as mqtt
import json
import sys
import time
import datetime
import threading

#BROKER_HOST="127.0.0.1"
BROKER_HOST="edgex"

# CONNECT & SUBSCRIBE
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    SRCTOPIC="command/"+DEV+"/#"
    client.subscribe(SRCTOPIC)

# PUBLISH CALLBACK
def on_message(client, userdata, msg):
    #ECHO MESSAGE
    print(msg.topic+" "+str(msg.payload))
    #PARSER
    cmd=msg.topic.split("/")
    #CRAFT TEST RESPONSE
    data = {
        "deviceName": DEV,
        "message": RES
    }
    resp=json.dumps(data)
    uid=msg.topic.split("/")[-1]
    topic="command/response/"+DEV+"/"+uid
    client.publish(topic, payload=resp)
    async_t = threading.Thread(target=gen_async_event,args=(client,))
    async_t.start()
    
# SIMULATE ASYNC EVENT    
def gen_async_event(client):
    topic="incoming/data/"+DEV+"/ping"; client.publish(topic, payload=None);
    time.sleep(2.5)
    event="heartbeat "+DEV+" "+str(datetime.datetime.now())
    topic="incoming/data/"+DEV+"/message";
    client.publish(topic, payload=event);

  
# MAIN
#seed(1)
# CHECK INPUT
DEV = sys.argv[1]
if len(sys.argv) < 3: RES="00000"
else: RES=sys.argv[2]
# LOOP
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("edgex", 1883, 60)
client.connect("edgex")

client.loop_forever()

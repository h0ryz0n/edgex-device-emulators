# MQTT DEVICE EMULATOR FOR EDGEX
## USAGE : spawn-mqtt.py <device_name>

# listen on topic: mosquitto_sub -d -h <host> -t <topic>
# listen on all: mosquitto_sub -d -h <host> -t "#"

#from random import seed
#from random import randint
import paho.mqtt.client as mqtt
import json
import sys

# CONNECT & SUBSCRIBE
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe("CommandTopic")
    #multilevel-hell
    SRCTOPIC="command/"+DEV+"/#"
    client.subscribe(SRCTOPIC)
    

# PUBLISH CALLBACK
def on_message(client, userdata, msg):
    #ECHO MESSAGE
    print(msg.topic+" "+str(msg.payload))
    #JSON PARSE
    #data = json.loads(msg.payload)
    #CRAFTING REPONSE
    #data['deviceName'] = "MQTT-test-device"
    #data['message'] = "this is a response TEST1"
    #resp = json.dumps(data)
    #client.publish("ResponseTopic", payload=resp)
    #client.publish("reponse/mqtt1rt0", payload=resp)
    #PARSER
    cmd=msg.topic.split("/")

    # IF LISTENS ALL
    # is for me?
    #if cmd[1]=="mqtt1":
        # is a command?
        #if cmd[0]=="command":
            # craft response
            #uid=msg.topic.split("/")[-1]
            #topic="command/response/mqtt1/"+uid
            #client.publish(topic, payload=None)
            #exit
            
    # IF LISTENS ONLY HIS TOPIC
    # craft a response
    data = {
        "deviceName": DEV,
        "message": RES
    }
    resp = json.dumps(data)
    uid=msg.topic.split("/")[-1]
    topic="command/response/"+DEV+"/"+uid
    client.publish(topic, payload=resp)


# CRAFT A RANDOM READING [da capire e fare a parte]
#randomdata = json.loads(msg.payload)
#client.publish("DataTopic", payload=randomdata)

# MAIN LOOP
#seed(1)

DEV = sys.argv[1]
if len(sys.argv) < 3: RES="test response"
else: RES=sys.argv[2]

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("edgex", 1883, 60)
client.connect("edgex")

client.loop_forever()

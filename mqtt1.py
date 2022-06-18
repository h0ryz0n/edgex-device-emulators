# MQTT DEVICE EMULATOR FOR EDGEX

# listen on topic: mosquitto_sub -d -h <host> -t <topic>
# listen on all: mosquitto_sub -d -h <host> -t "#"

#from random import seed
#from random import randint
import paho.mqtt.client as mqtt
import json

# CONNECT & SUBSCRIBE
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe("CommandTopic")
    #multilevel-hell
    client.subscribe("command/mqtt1/#")
    

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

    # is for me?
    if cmd[1]=="mqtt1":
        # is a command?
        if cmd[0]=="command":
            # craft response
            uid=msg.topic.split("/")[-1]
            topic="command/response/mqtt1/"+uid
            client.publish(topic, payload=None)
            exit


# CRAFT A RANDOM READING [da capire e fare a parte]
#randomdata = json.loads(msg.payload)
#client.publish("DataTopic", payload=randomdata)

# MAIN LOOP
#seed(1)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("edgex", 1883, 60)
client.connect("edgex")

client.loop_forever()

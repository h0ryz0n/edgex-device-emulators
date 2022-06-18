# MQTT DEVICE EMULATOR FOR EDGEX
#from random import seed
#from random import randint
import paho.mqtt.client as mqtt
import json

# CONNECT & SUBSCRIBE
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe("CommandTopic/#")
    client.subscribe("CommandTopic")

# PUBLISH CALLBACK
def on_message(client, userdata, msg):
    #ECHO MESSAGE
    print(msg.topic+" "+str(msg.payload))
    #JSON PARSE
    data = json.loads(msg.payload)
    #CRAFTING REPONSE
    #data['deviceName'] = "MQTT-test-device"
    data['message'] = "this is a response TEST1"
    resp = json.dumps(data)
    #client.publish("ResponseTopic", payload=resp)
    client.publish("rt0", payload=resp)
    #client.publish("dt0", payload=resp)

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

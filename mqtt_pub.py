import paho.mqtt.client as mqtt
import json

TOPIC = "test" 
client = mqtt.Client()
client.connect("localhost")

xxx = {"hello":"hello"}

payload = json.dumps(xxx).encode('utf-8')

client.publish(TOPIC, payload=payload, qos=0, retain=False)


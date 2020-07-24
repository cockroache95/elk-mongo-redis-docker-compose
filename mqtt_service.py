import paho.mqtt.client as mqtt
import time
import logging
import json
import asyncio
from threading import Thread, Lock

mqttControlClient = mqtt.Client()
PING_INTERVAL = 3
PING_MAX_DURATION = PING_INTERVAL * 3
PING_CONTENT = {"type": "PING"}
PING_SYNC_TOPIC = "PING_SYNC_TOPIC"
MQTT_ADDRESS = "localhost"
MQTT_PORT = 1883
mqttControlPingTime = time.time()
mqttlog = logging.getLogger("MQTT")
TOPIC = "test"
running = True

def mqttControlPingProc():
    global mqttControlPingTime
    while running:
        current = time.time()
        if mqttControlClient.is_connected():
            if current - mqttControlPingTime > PING_MAX_DURATION:
                print("mqttControlClient resubscribe!")
                mqttlog.warning("mqttControlClient resubscribe!")
                mqttControlClient.subscribe(TOPIC)
                mqttControlClient.message_callback_add(
                    TOPIC, onMessage)

                mqttControlClient.subscribe(PING_SYNC_TOPIC)
                mqttControlClient.message_callback_add(
                    PING_SYNC_TOPIC, onPingPongCallBack)


                mqttControlPingTime = time.time()
            mqttControlClient.publish(
                PING_SYNC_TOPIC, json.dumps(PING_CONTENT))
        time.sleep(PING_INTERVAL)

def mqttControlPingProc_worker(loop):
    asyncio.set_event_loop(loop)
    loop.create_task(mqttControlPingProc())
    loop.run_forever()

def mqttControlProc():
    while running:
        try:
            mqttlog.info("Connecting to mqtt control server ...")
            mqttControlClient.connect(
                MQTT_ADDRESS, MQTT_PORT, 5)
        except Exception as e:
            print(e)
            mqttlog.error("Control connection failed!")
            continue
        break
    mqttlog.info("Control connection successful!")
    mqttControlClient.subscribe(TOPIC)
    mqttControlClient.message_callback_add(
        TOPIC, onMessage)
    
    mqttControlClient.subscribe(PING_SYNC_TOPIC)
    mqttControlClient.message_callback_add(
        PING_SYNC_TOPIC, onPingPongCallBack)

    mqttControlClient.loop_forever()

def mqttControlProc_worker(loop):
    asyncio.set_event_loop(loop)
    loop.create_task(mqttControlProc())
    loop.run_forever()
      
def onPingPongCallBack(client, userdata, message):
    global mqttControlPingTime
    msg = message.payload.decode()
    jsonData = json.loads(msg)
    if "type" not in jsonData:
        return
    if jsonData["type"] == "PING":
        mqttControlPingTime = time.time()
        return
          
def onMessage(client, userdata, message):
    msg = message.payload.decode()
    jsonData = json.loads(msg)
    print(jsonData)

mqttControlProc_worker_loop = asyncio.new_event_loop()
mqttControlProc_worker = Thread(target=mqttControlProc_worker,
                        args=(mqttControlProc_worker_loop,))
mqttControlProc_worker.start()
print("Thread mqttControlProc Init Successfully")

mqttControlPingProc_worker_loop = asyncio.new_event_loop()
mqttControlPingProc_worker = Thread(target=mqttControlPingProc_worker,
                        args=(mqttControlPingProc_worker_loop,))
mqttControlPingProc_worker.start()

while True:pass





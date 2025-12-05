import paho.mqtt.client as mqtt
from pathlib import Path
from datetime import datetime
import utility
import asyncio
import websockets.exceptions as exception

broker = '192.168.1.19'
port = 1883
topicCommand = "esp32/command"
topicFeedback = "esp32/response"
client_id = f'guest-server'

nomeFileLog="./logEsp32.log"

listWaitedUser=[]

# Configurazione del server MQTT
# The calbalck for when the client receives a connection acknowledgement response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topicFeedback)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+payloadToStr(msg.payload))
    if len(listWaitedUser)>0:
        try:
            asyncio.run(utility.sendTo(listWaitedUser.pop(0).websocket, ("R:-"+payloadToStr(msg.payload))))
        except exception.ConnectionClosed:
            print("utente disconnesso prima di ricevere il messaggio")
            
    percorso=Path(nomeFileLog)
    if(not percorso.exists()):
        with open(nomeFileLog, 'w') as file:
            saveInFile(file, msg.payload)
    else:
         with open(nomeFileLog, 'a') as file:
            saveInFile(file, msg.payload)

def saveInFile(file, payload):
    payload=payloadToStr(payload)
    file.write(datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S.%f")+" => "+payload+"\n")

def payloadToStr(payload):
    payload=str(payload).removeprefix("b'")
    payload=payload.removesuffix("'")
    return payload


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(broker, port)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_start()

def sendCommand(message, user):
    #inviamo il messaggio e aspettiamo che venga ricevuto
    mqttc.publish(topicCommand, message).wait_for_publish()
    listWaitedUser.append(user)

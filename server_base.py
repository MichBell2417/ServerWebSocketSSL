import asyncio
import websockets
import ssl
import pathlib
import utility
import mosquitto as mqttClient
from datetime import datetime

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).parent / "certificatoSSL" / "localhost.pem"
#fullchain_pem = pathlib.Path("/etc/letsencrypt/live/michy.sytes.net/fullchain.pem")
#privkey_pem = pathlib.Path("/etc/letsencrypt/live/michy.sytes.net/privkey.pem")
ssl_context.load_cert_chain(localhost_pem)
#ssl_context.load_cert_chain(fullchain_pem, privkey_pem)

separator=":-"

async def manager(websocket):
    print("connected")
    async for message in websocket:
        messageParts=message.split(separator)
        if(messageParts[0]=="M"):
            if(utility.messaggio(messageParts)):
                #la struttura del messaggio è corretta
                if messageParts[3]=="ChronDoor":
                    with open(mqttClient.nomeFileLog, "r") as log:
                        await utility.sendTo(websocket, "R:-"+log.read())
                else:
                    command=utility.changeToMqttMessage(messageParts)
                    mqttClient.sendCommand(command, utility.userFromWebsocket(websocket))
            else:
                await utility.sendTo(websocket, "R:-E1")
        elif(messageParts[0]=="A"):
            if(utility.accesso(messageParts[1],messageParts[2],websocket)):
                print("logged in")
                await utility.sendTo(websocket, ("U:-OK:-"+str(utility.userFromWebsocket(websocket).secureC)))
            else:
                await utility.sendTo(websocket, "U:-E0")
    utility.removeOnlineUser(websocket)
    print("disconnected")

async def start():
    async with websockets.serve(manager, "", 8080, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(start())

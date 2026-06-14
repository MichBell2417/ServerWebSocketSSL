import asyncio
import websockets
import ssl
import pathlib
import utility
import mosquitto as mqttClient
from datetime import datetime
import signal
import sys

#path="/etc/letsencrypt/live/michy.sytes.net"
path=pathlib.Path(__file__).parent / "certificatoSSL"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#localhost_pem = pathlib.Path(__file__).parent / "certificatoSSL" / "localhost.pem"
fullchain_pem = pathlib.Path(path / "fullchain.pem")
privkey_pem = pathlib.Path(path / "privkey.pem")
#ssl_context.load_cert_chain(localhost_pem)
ssl_context.load_cert_chain(fullchain_pem, privkey_pem)

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

# ---------------- MQTT pump asyncio ----------------
_mqtt_pump_task = None
_mqtt_pump_running = False

async def mqtt_pump(poll_interval: float = 0.1):
    global _mqtt_pump_running
    mqttc = mqttClient.mqttc
    _mqtt_pump_running = True
    while _mqtt_pump_running:
        try:
            mqttc.loop(timeout=poll_interval)
        except Exception as e:
            print("mqtt_pump: loop error:", e)
            await asyncio.sleep(1.0)
            continue
        await asyncio.sleep(poll_interval)

def start_mqtt_pump(loop: asyncio.AbstractEventLoop, poll_interval: float = 0.1):
    global _mqtt_pump_task
    try:
        mqttClient.init_client()
    except Exception as e:
        print("start_mqtt_pump: init_client error:", e)
    _mqtt_pump_task = loop.create_task(mqtt_pump(poll_interval))

async def stop_mqtt_pump():
    global _mqtt_pump_running, _mqtt_pump_task
    _mqtt_pump_running = False
    if _mqtt_pump_task is not None:
        try:
            await asyncio.wait_for(_mqtt_pump_task, timeout=2.0)
        except asyncio.TimeoutError:
            _mqtt_pump_task.cancel()
            try:
                await _mqtt_pump_task
            except Exception:
                pass
    try:
        mqttClient.stop_client()
    except Exception as e:
        print("stop_mqtt_pump: stop_client error:", e)

async def start():
    print("starting websocket")
    loop = asyncio.get_running_loop()
    start_mqtt_pump(loop, poll_interval=0.1)
    async with websockets.serve(manager, "0.0.0.0", 8080, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print("started")
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(s, lambda sig, frame, sname=s: (print(f"Received {sname}, shutting down..."), sys.exit(0)))
        except Exception:
            pass

    try:
        asyncio.run(start())
    except SystemExit:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(stop_mqtt_pump())
            loop.close()
        except Exception as e:
            print("Cleanup error:", e)
    except KeyboardInterrupt:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(stop_mqtt_pump())
            loop.close()
        except Exception as e:
            print("Cleanup error:", e)


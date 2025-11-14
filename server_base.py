import asyncio
import websockets
import ssl
import pathlib
import utility

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
            if(utility.messaggio()):
                #la struttura del messaggio è corretta
                print(messageParts[1])
            else:
                await utility.sendTo(websocket, "R:-E1")
        elif(messageParts[0]=="A"):
            if(utility.accesso(messageParts)):
                print("logged in")
            else:
                await utility.sendTo(websocket, "U:-E0")
        
    print("disconnected")

async def start():
    async with websockets.serve(manager, "", 8080, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(start())

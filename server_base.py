import asyncio
import websockets
import ssl
import pathlib

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).parent / "certificatoSSL" / "localhost.pem"
ssl_context.load_cert_chain(localhost_pem)

async def manager(websocket):
    print("connected")
    async for message in websocket:
        print(message)
    print("disconnected")

async def start():
    async with websockets.serve(manager, "", 8080, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(start())
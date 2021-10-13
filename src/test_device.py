import asyncio
import websockets
import logging
import ssl
import pathlib

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

#local_ca = pathlib.Path("/Users/ay31278-dev/Library/Application Support/mkcert/rootCA.pem")
#local_ca_key = pathlib.Path("/Users/ay31278-dev/Library/Application Support/mkcert/rootCA-key.pem")

#ssl_context = ssl.SSLContext()
#ssl_context.load_cert_chain(local_ca, local_ca_key)

api_key="NkBBRDdxZnkhMQ"
#ws_url=f"wss://api.websocket.local/ws/devices/{api_key}"
ws_url=f"ws://localhost:8080/ws/devices/{api_key}"
ssl_context = None

async def listen(websocket):
    while True:
        _data = await websocket.recv()
        logger.info(_data)

async def main():
    async for websocket in websockets.connect(ws_url):
        try:
            logger.info("CONNECTED")
            await asyncio.gather(
                listen(websocket)
            )
        except websockets.ConnectionClosed:
            logger.error("CONNECTION CLOSE")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

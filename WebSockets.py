import asyncio

import websockets

# create handler for each connection


async def handler(websocket, path):

    data = await websocket.recv()

    reply = f"Data recieved as:  {data}!"

    await websocket.send(reply)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())

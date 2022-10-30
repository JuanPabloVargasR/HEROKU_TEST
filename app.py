import asyncio
import signal
import os
import json

import websockets

from SortingAlgorithms import *


async def handler(websocket):

    while True:

        request = await websocket.recv()

        algorithms = {"Mergesort": merge_sort,
                      "Heapsort": heap_sort,
                      "QuicksortRight": quick_sort_right,
                      "QuicksortLeft": quick_sort_left}

        data = json.loads(request)

        array = data["array"]
        algorithm = algorithms[data["algorithm"]]

        await algorithm(array)

        message = json.dumps({"array": array})

        await websocket.send(message)


async def main():

    # Set the stop condition when receiving SIGTERM.

    loop = asyncio.get_running_loop()

    stop = loop.create_future()

    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        handler,

        host="",

        port=int(os.environ["PORT"]),

    ):
        await stop


if __name__ == "__main__":

    asyncio.run(main())

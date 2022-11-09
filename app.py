import asyncio
import signal
import os
import json

import websockets

from SortingAlgorithms import *


async def merge_sort(websocket, array):

    await websocket.send(array)

    if len(array) > 1:

        mid = len(array) // 2

        left = array[:mid]
        right = array[mid:]

        await merge_sort(left)
        await merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):

            if left[i] < right[j]:

                array[k] = left[i]
                i += 1

            else:

                array[k] = right[j]
                j += 1

            k += 1

        while i < len(left):

            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):

            array[k] = right[j]
            j += 1
            k += 1

    return array


async def handler(websocket):

    while True:

        request = await websocket.recv()

        message = json.dumps(type(websocket))

        await websocket.send(message)

        '''

        algorithms = {"Mergesort": merge_sort,
                      "Heapsort": heap_sort,
                      "QuicksortRight": quick_sort_right,
                      "QuicksortLeft": quick_sort_left}

        data = json.loads(request)

        array = data["array"]
        algorithm = algorithms[data["algorithm"]]

        message = json.dumps({"array": algorithm(websocket, array)})

        await websocket.send(message)
        '''


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

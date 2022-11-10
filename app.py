import asyncio
import signal
import os
import json

import websockets

from SortingAlgorithms import *


async def merge_sort(websocket, array):

    if len(array) > 1:

        # middle of the array
        mid = len(array) // 2

        # partitions the array into two halves (left and right)
        left = array[:mid]
        right = array[mid:]

        # sends the partitions to the client
        await websocket.send(json.dumps({"message": f"array: {array}, left: {left}, right: {right}"}))

        # recursively sort the left and right halves
        await merge_sort(websocket, left)
        await merge_sort(websocket, right)

        # i is the index of the left array, j is the index of the right array, k is the index of the merged array
        i = j = k = 0

        # while there are elements in both left and right arrays
        while i < len(left) and j < len(right):
            # if the left element is smaller than the right element
            if left[i] < right[j]:
                # set the left element to the merged array
                array[k] = left[i]
                # increment the index of the left array
                i += 1
            # else if the right element is smaller than the left element (or they are equal)
            else:
                # set the right element to the merged array
                array[k] = right[j]
                # increment the index of the right array
                j += 1
            # increment the index of the merged array
            k += 1

        # one of the arrays has been fully merged, so we add the remaining elements of the other array to the merged array
        # it is safe to assume that the remaining elements are already sorted and that they are greater than the last element of the merged array
        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

        # sends the merged array to the client
        await websocket.send(json.dumps({"message": f"left: {left}, right: {right}, merge: {array}"}))


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

        await algorithm(websocket, array)

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

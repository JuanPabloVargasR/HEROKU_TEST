import asyncio
import signal
import os
import json

import websockets

from SortingAlgorithms import quick_sort_left, quick_sort_right


async def merge_sort(websocket, array: list):

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


async def heap_sort(websocket, arr: list):

    async def heapify(arr: list, n: int, i: int):

        # initialy assume the largest element is the root
        largest = i
        # the left child of the root is in the position 2 * i + 1 if it exists
        l = 2 * i + 1
        # the right child of the root is in the position 2 * i + 2 if it exists
        r = 2 * i + 2

        # if the left child exists and is greater than the root
        if l < n and arr[i] < arr[l]:
            # set the left child as the largest element
            largest = l

        # if the right child exists and is greater than the largest element
        if r < n and arr[largest] < arr[r]:
            # set the right child as the largest element
            largest = r

        # if the largest element was not the root
        if largest != i:
            # swap the largest element with the root
            arr[i], arr[largest] = arr[largest], arr[i]
            # recursively heapify the affected sub-tree (the position from which the largest element was swapped)
            await heapify(arr, n, largest)

    # length of the array
    n = len(arr)

    # build a max heap by heapifying the non-leaf nodes
    for i in range(n//2, -1, -1):
        await heapify(arr, n, i)

    # sends the max heap to the client
    await websocket.send(json.dumps({"message": f"max heap created: {arr}"}))

    # extract the root which is the largest element and swap it with the last element not yet sorted
    for i in range(n - 1, 0, -1):
        # sends a message to the client with the swapped elements
        websocket.send(json.dumps(
            {"message": f"extracting root {arr[0]} and swapping with {arr[i]}"}))
        arr[i], arr[0] = arr[0], arr[i]
        # sends a message to the client with the sorted elements
        await websocket.send(json.dumps({"message": f"sorted elements: {arr[:i]}"}))
        # sends a message to the client with the unsorted elements to heapify
        await websocket.send(json.dumps({"message": f"heapify {arr[i:]}"}))
        # discard the sorted element from the heap and heapify the new root
        await heapify(arr, i, 0)
        # sends a message to the client with the new max heap
        await websocket.send(json.dumps({"message": f"max heap created: {arr[i:]}"}))


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

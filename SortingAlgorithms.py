def quick_sort_right(arr: list) -> list:
    def partition(arr: list, low: int, high: int) -> int:
        i = (low - 1)
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return (i + 1)

    def quick_sort_helper(arr: list, low: int, high: int) -> list:
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)
    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def quick_sort_left(arr: list) -> list:
    def partition(arr: list, low: int, high: int) -> int:
        i = low
        pivot = arr[low]
        for j in range(low + 1, high + 1):
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i], arr[low] = arr[low], arr[i]
        return i

    def quick_sort_helper(arr: list, low: int, high: int) -> list:
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)
    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr

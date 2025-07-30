def binary_search(mylist, n):
    low = 0
    high = len(mylist) - 1
    while low <= high:
        mid = (low + high) // 2 
        if n > mylist[mid]:
            low = mid + 1
        elif n < mylist[mid]:
            high = mid - 1
        else:
            return mid
    return -1

mylist = [12, 22, 30, 39, 45, 54]
n = 54
result = binary_search(mylist, n)

if result != -1:
    print(f'Element found at index: {result}')
else:
    print('Element not found!')

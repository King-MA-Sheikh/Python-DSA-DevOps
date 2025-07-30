def selection_sort(array):
    n = len(array)
    for i in  range(n-1):
        mini = i
        for j in range(i+1,n):
            if array[j] < array[mini]:
                mini = j
            array[i], array[mini] = array[mini],array[i]

array = [24,41,33,42,17]
print(f'Before Sorting: {array}')
selection_sort(array)
print(f'After Sorting: {array}')
print("Thank You")

import random
import time


def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1


def binarysearch(l, target, low = None, high = None):
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1

    if high < low:
        return -1
    midpoint = (low + high) // 2

    if  l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binarysearch(l, target, low, midpoint - 1)
    else:
        return binarysearch(l, target, midpoint+1, high)
    
if __name__ == '__main__':
    l = [1, 3, 5, 10, 12]
    target = 10
    print(naive_search(l, target))
    print(binarysearch(l, target))

    length = 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))
    sorted_list = sorted(list(sorted_list))

    start = time.time()
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("naive search time: ", (end - start)/length, "seconds")

    start = time.time()
    for target in sorted_list:
        binarysearch(sorted_list, target)
    end = time.time()
    print("binary search time: ", (end - start)/length, "seconds")
     






    


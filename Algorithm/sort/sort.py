# coding=utf-8
import time
import random
from copy import deepcopy

"""
list
57, 82, 85, 78, 66, 75, 7, 87
 
### key = 85 , 依次与list[1],list[0]比较，key小则互换位置。
"""


def costTime(func):
    def wrapper(*args, **kwargs):
        tstart = time.time()
        res = func(*args, **kwargs)
        print("cost time:", time.time() - tstart)
        return res

    return wrapper


def gene_random_list(n=8):
    data = []
    for i in range(n):
        data.append(random.randint(1, n))
    return data


@costTime
def insert(data):
    n_len = len(data)
    if n_len < 2:
        return data
    if n_len == 2:
        if data[0] > data[1]:
            data[0], data[1] = data[1], data[0]
        return data
    for i in range(2, n_len):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            j = j - 1
    return data


# @costTime
def fast(data):
    n_len = len(data)
    if n_len <= 1:
        return data
    mid = n_len // 2
    less = [data[i] for i in range(n_len) if data[i] < data[mid] and i != mid]
    gret = [data[j] for j in range(n_len) if data[j] > data[mid] and j != mid]
    return fast(less) + [data[mid]] + fast(gret)


def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)


def merge(left, right):
    l, r = 0, 0
    sort_list = []
    while l < len(left) and r < len(right):
        # print(left, right)
        if left[l] < right[r]:
            sort_list.append(left[l])
            l = l + 1
        else:
            sort_list.append(right[r])
            r = r + 1
    sort_list += left[l:]
    sort_list += right[r:]
    return sort_list


def main():
    data = gene_random_list(80000)
    # print("data:", data)
    insert(data)
    # print(data)
    data2 = deepcopy(data)
    print("id:", id(data2))
    tstart = time.time()
    sdata = fast(data2)
    print("fast cost time:", time.time() - tstart)

    print("id:", id(data2))
    tstart = time.time()
    sdata = merge_sort(data2)
    print("merge cost time:", time.time() - tstart)
    # print(sdata)
    pass


if __name__ == '__main__':
    main()

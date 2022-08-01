# coding=utf-8
"""
基数排序
原始数据: [817, 184, 714, 211, 934, 608, 71, 867, 130, 107]
0 轮  个位数排序
[[130], [211, 71], [], [], [184, 714, 934], [], [], [817, 867, 107], [608], []]
[130, 211, 71, 184, 714, 934, 817, 867, 107, 608]
1 轮  十位数排序
[[107, 608], [211, 714, 817], [], [130, 934], [], [], [867], [71], [184], []]
[107, 608, 211, 714, 817, 130, 934, 867, 71, 184]
2 轮  百位数排序
[[71], [107, 130, 184], [211], [], [], [], [608], [714], [817, 867], [934]]
[71, 107, 130, 184, 211, 608, 714, 817, 867, 934]
[71, 107, 130, 184, 211, 608, 714, 817, 867, 934]
"""
import random


def radixSort(arr, radis_len):
    """
    :param arr:
    :param radis_len:
    :return:
    """

    for k in range(radis_len):
        print(k, "轮")
        s = [[] for _ in range(10)]
        for i in arr:
            s[i//(10**k) % 10].append(i)
        arr = [a for b in s for a in b]
        print(s)
        print(arr)
    return arr


if __name__ == "__main__":
    A = [random.randint(1, 999) for i in range(10)]
    print("原始数据:", A)
    print(radixSort(A, 3))
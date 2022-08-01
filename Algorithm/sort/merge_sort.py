# coding=utf-8
"""
分裂：
    46 3 82 90 56 17 95
    每次从 len(list)//2开始	
    46 3 82 90      56 17 95
    46 3  82 90    56 17   95
归并：
    46 3  82 90    56 17   95
    3 46   82 90    17 56   95
    3 46 82 90      17 56 95
    3 17 46 52 82 90 95
"""

class MergeSort(object):
    def __init__(self, numbers):
        self.values = numbers
        self.count = len(numbers)

    def sort(self):
        self.merge_sort(0, self.count - 1)
        return self.values

    def merge_sort(self, low, high):
        if low < high:
            mid = (low + high) // 2

            self.merge_sort(low, mid)
            self.merge_sort(mid + 1, high)
            self.merge(low, mid, high)

    def merge(self, low, mid, high):
        b = []
        i = low
        j = mid + 1

        while i <= mid and j <= high:
            if self.values[i] <= self.values[j]:
                b.append(self.values[i])
                i += 1
            else:
                b.append(self.values[j])
                j += 1

        while i <= mid:
            b.append(self.values[i])
            i += 1

        while j <= high:
            b.append(self.values[j])
            j += 1

        for index, val in enumerate(b):
            self.values[low + index] = val

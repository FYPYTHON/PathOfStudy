# coding=utf-8
from functools import reduce

num = [1, 2, 3]
nums = [num for i in range(3)]


def all_aa(nums):
    mfunc = lambda x, y: ["%s%s" % (i, j) for i in x for j in y]

    # reduce(mfunc, nums)
    # result1 = mfunc(nums[0], nums[1])
    # result2 = mfunc(result1, nums[2])

    dataresult = reduce(mfunc, nums)

    print(dataresult)
    print(len(dataresult))


def all_a(nums):
    mfunc = lambda x, y: ["%s%s" % (i, j) for i in x for j in y if i != j if not str(j) in str(i)]
    dataresult = reduce(mfunc, nums)
    print(dataresult)
    print(len(dataresult))


def creverse(nums, i, j):
    while i < j:
        # print(i, j)
        temp = nums[i]
        nums[i] = nums[j]
        nums[j] = temp
        i += 1
        j -= 1

def csort(nums, n):
    if n == 1: return
    maxC = 0
    maxI = 0

    for i in range(n):
        if nums[i] > maxC:
            maxC = nums[i]
            maxI = i
    print(n-1, maxI, nums)
    creverse(nums, 0, maxI)
    creverse(nums, 0, n-1)

    csort(nums, n - 1)


if __name__ == '__main__':
    # all_a(nums)
    num = [1, 6, 7, 4, 5, 2, 3]
    # creverse(num, 2, 5)
    csort(num, 7)
    print(num)

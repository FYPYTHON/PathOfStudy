# coding=utf-8
nums = [1, 2, 5, 9, 14, 30, 44, 67]


def binarySearch(nums, target):
    if len(nums) <= 0: return -1
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        else:
            return mid
    return -1


binarySearch(nums, 14)

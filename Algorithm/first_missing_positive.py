# coding=utf-8
import pdb
pdb.set_trace()
"""
Given an unsorted integer array, find the smallest missing positive integer.
"""
# nums = [1, 2, 0]  # 3
# nums = [3, 4, -1, 1]  # 2
# nums = [7, 8, 9, 11, 12]  # 1
# nums = [1, 2, 3, 4]  # 5
# nums = [-1, 2, 1, 3, 5] #4
nums = [1,2,3,10,2147483647,9] #4

class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) < 1:
            return 1
        if len(nums) == 1:
            return 1 if nums[0] != 1 else 2
        positive = [i for i in nums if i > 0]
        if len(positive) < 1:
            return 1
        temp = 0
        for i in sorted(positive):
            if (i-temp) > 1:
                return temp + 1
            else:
                temp = i
        return temp + 1

class Solution1(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) < 1:
            return 1
        if len(nums) == 1:
            return 1 if nums[0] != 1 else 2
        for i in range(1, len(nums)+1):
            if i not in nums:
                return i
        return len(nums) + 1

if __name__ == "__main__":
    so = Solution1()
    print(so.firstMissingPositive(nums))
    print(a)
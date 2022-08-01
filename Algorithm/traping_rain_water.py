# coding=utf-8
"""
Given n non-negative integers representing an elevation map where the width of each bar is 1,
compute how much water it is able to trap after raining.

The above elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1].
In this case, 6 units of rain water (blue section) are being trapped. Thanks Marcos for contributing this image!
Example:
Input: [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
"""
nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]  # 6
# nums = [2, 0, 2]  # 2
# nums = [5, 4, 1, 2]
# nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
#     __             __
#  __|  |         __|  |    __
# |  |  |__    __|     |   |  |__
# |__|__|__|__|________|___|_____|__________

nums = [4, 2, 3]
nums = [5, 2, 1, 2, 1, 5]

class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
    def trap1(self, height):
        ans = 0
        h1 = 0
        h2 = 0
        for i in range(len(height)):
            h1 = max(h1, height[i])
            h2 = max(h2, height[-i - 1])
            ans = ans + h1 + h2 - height[i]
        return ans - len(height) * h1


class Solution1(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        i = 0
        j = len(height) - 1

        leftMax = 0
        rightMax = 0

        r = 0
        while i < j:
            if height[i] < height[j]:
                if leftMax < height[i]:
                    leftMax = height[i]
                else:
                    r += leftMax - height[i]
                i += 1
            else:
                if rightMax < height[j]:
                    rightMax = height[j]
                else:
                    r += rightMax - height[j]
                j -= 1
        return r


so = Solution()
print(so.trap1(nums))
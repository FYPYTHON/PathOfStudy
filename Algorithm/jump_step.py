# coding=utf-8
import time


# nums = [2, 3, 1, 1, 4]
# nums = [1, 2, 3]
# nums = [2, 0, 1]
# nums = [1, 1, 1, 1]
nums = [2, 1, 1, 1, 1]


class Solution(object):
    def jump(self, nums):
        """
        nums = [2,3,1,1,4]
        数组的每一项为能跳跃的步数，求最小跳跃次数到达数组末端。
        :type nums: List[int]
        :rtype: int
        """
        length = len(nums)
        index = 0
        count = 0
        if length <= 1:
            return count
        while True:
            if nums[index] >= length - 1 - index:
                count += 1
                return count
            max = 0
            tmp = 0
            for i in range(1, nums[index] + 1):
                if i + nums[i + index] > max:
                    max = i + nums[i + index]
                    tmp = i + index
            index = tmp
            count += 1


if __name__ == "__main__":
    start = time.time()
    so = Solution()
    print(so.jump(nums))
    end = time.time()
    print("time:", end - start)
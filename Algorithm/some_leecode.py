#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 14:06
# @Author  : 1823218990qq.com
# @File    : erasecover.py
# @Software: PyCharm
from kazoo import client


class Solution:
    def eraseOverlapIntervals(self, intervals):
        if not intervals:
            return 0
        intervals.sort(key=lambda x: x[1])
        count = 0
        start_point = intervals[0][1]
        for i in range(0, len(intervals) - 1):
            if start_point > intervals[i + 1][0]:
                count += 1
            else:
                start_point = intervals[i + 1][1]
        return count


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def print(self):
        print(self.val)
        # if self.next is None:
        #     return ("{} {}".format(self.val, None))
        # else:
        #     return ("{} {}".format(self.val, self.next))


class Solution1:
    """
    # s = Solution()
    # # 24 + 17
    # print("24 + 17")
    # l4 = ListNode(2, None)
    # l2 = ListNode(4, l4)
    # l5 = ListNode(5, l2)
    #
    # l1 = ListNode(1, None)
    # l7 = ListNode(7, l1)
    # l6 = ListNode(6, l7)
    # s1 = Solution1()
    # s1.addTwoNumbers(l5, l1)
    """

    def printListNode(self, node: ListNode):
        strv = ""
        while node is not None:
            strv = str(node.val) + strv
            node = node.next
        print("node v:", strv)

    def addTwoNumbers(self, l1: ListNode, l2: ListNode):
        self.printListNode(l1)
        self.printListNode(l2)
        # pass
        #
        # str1 = ""
        # str2 = ""
        #
        # while True:
        #     print("l1", l1.val)
        #     str1 = str(l1.val) + str1
        #     l1 = l1.next
        #     if l1 is None:
        #         break
        # print("str1:", str1)
        #
        # while True:
        #     print("l2", l2.val)
        #     str2 = str(l2.val) + str2
        #     l2 = l2.next
        #     if l2 is None:
        #         break
        # print("str2:", str2)
        # v3 = str(int(str1) + int(str2))
        # print(v3)
        # return v3

        sp = 0
        cend = True
        node = None
        tnode = None
        while cend:

            if l1 is None and l2 is None:
                cend = False
                break
            # print(l1.val, l2.val)

            v1 = v2 = 0
            if l1 is not None:
                v1 = l1.val
                l1 = l1.next
            if l2 is not None:
                v2 = l2.val
                l2 = l2.next

            sum = 0
            if v1 + v2 > 9:
                if sp > 0:
                    sum = v1 + v2 - 10 + 1
                else:
                    sum = v1 + v2 - 10
                sp = 1
            else:
                if sp > 0:
                    sum = v1 + v2 + 1
                else:
                    sum = v1 + v2
                sp = 0
            print(sum)
            if node is None:
                node = ListNode(sum, None)
            else:
                if tnode is None:
                    tnode = ListNode(sum, None)
                    node.next = tnode
                else:
                    tnode.next = ListNode(sum, None)
                    tnode = tnode.next

        self.printListNode(node)


def findMedianSortedArrays(self, nums1, nums2) -> float:
    cc = sorted(nums1 + nums2)
    length = len(cc)
    # print(cc)
    if length % 2 == 1:
        return cc[length // 2]
    else:
        return (cc[length // 2] + cc[length // 2 - 1]) * 1.0 / 2


def lengthOfLongestSubstring(self, s: str) -> int:
    """
    s1 = "abcabc"
    s2 = 'dvdf'
    s3 = 'bbbbb'
    s4 = 'pwwkew'
    sb = lengthOfLongestSubstring("", s4)
    print(sb)
    """
    pos = 0
    maxlen = 0
    curlen = 0
    for i in range(len(s)):
        """
        a     b       c      a      b      c
        pos                  
                             i
        s[pos:i] = a b c
        curlen = 3 - 0 - 0
        pos = 0 + 0 + 1
              pos                   i
        s[pos:i] = b c a
        curlen = 4 - 1 - 0
        pos = 1 + 0 + 1
        """
        # print(s[i], s[pos:i], pos, i)
        if s[i] in s[pos:i] and curlen > 0:
            if curlen > maxlen:
                maxlen = curlen
            curlen = i - pos - s[pos:i].index(s[i])
            pos = pos + s[pos:i].index(s[i]) + 1
        else:
            curlen += 1
        # print(i, pos, curlen, maxlen)
    if curlen > maxlen:
        return curlen
    else:
        return maxlen


#
def convert(self, s: str, numRows: int) -> str:
    """
    z1 = 'LEETCODEISHIRING'
    z2 = "PAYPALISHIRING"
    z3 = "AB"
    zz = convert("", z3, 2)
    print(zz)
    """
    # if numRows <= 1: return s
    # step = numRows * 2 - 2
    # slen = len(s)
    # znum = slen // step if slen % step == 0 else slen // step + 1
    # news = ""
    # for row in range(numRows):
    #     if row == 0:
    #         for i in range(znum):
    #             news += s[i*step]
    #     elif 0 < row < numRows - 1:
    #         for i in range(znum):
    #             if row + i*step < slen:
    #                 news += s[row + i*step]
    #             if row + i*step + (numRows - row - 1) * 2 < slen:
    #                 news += s[row + i*step + (numRows - row - 1) * 2]
    #     else:
    #         for i in range(znum):
    #             if numRows-1 + i*step < slen:
    #                 news += s[numRows-1 + i*step]
    # return news
    """
    s = 'LEETCODEISHIRING' numRows = 3
    L   C   I   R
    E T O E S I I G
    E   D   H   N
    """
    if numRows == 1 or numRows >= len(s):
        return s
    index = 0
    step = 1
    L = ['' for _ in range(numRows)]
    for x in s:
        L[index] += x
        if index == 0:
            step = 1
        elif index == numRows - 1:
            step = -1
        index += step
    print(L)
    return ''.join(L)



# str reverse [::-1]
def reverse(self, x: int) -> int:
    if x < 0:
        xs = int("-" + str(-x)[::-1])
        return xs if xs > -2 ** 31 - 1 else 0
    else:
        xs = int(str(x)[::-1])
        return 0 if xs > 2 ** 31 - 1 else xs


def threeSumClosest(self, nums, target: int) -> int:
    n = len(nums)
    nums.sort()  # 排序
    ans = float('inf')

    for first in range(n - 2):  # 枚举第一个元素
        if first > 0 and nums[first] == nums[first - 1]: continue  # 保证first不会有重复

        second, third = first + 1, n - 1
        max_sum = nums[first] + nums[-2] + nums[-1]
        min_sum = nums[first] + nums[first + 1] + nums[first + 2]
        if max_sum <= target:  # 最大的数
            if abs(max_sum - target) < abs(ans - target):
                ans = max_sum
            continue
        elif min_sum >= target:  # 最小的数
            if abs(min_sum - target) < abs(ans - target):
                ans = min_sum
            break

        while second < third:
            two_sum_target = target - nums[first]
            s = nums[second] + nums[third]
            if abs(s + nums[first] - target) < abs(ans - target):
                ans = s + nums[first]
            if s > two_sum_target:  # 当前数值太大 右指针左移
                third -= 1
                while third > second and nums[third] == nums[third + 1]:
                    third -= 1
            elif s < two_sum_target:  # 当前数值太小 左指针右移
                second += 1
                while third > second and nums[second] == nums[second - 1]:
                    second += 1
            else:  # 刚好等于 直接返回target即可
                return target
    return ans


def fourSum(self, nums, target: int):
    pass


from typing import List
def findCircleNum(self, M: List[List[int]]) -> int:
    N = len(M)
    count = 0
    visited = set()

    def dfs(i):
        for j in range(N):
            if M[i][j] and j not in visited:
                visited.add(j)
                dfs(j)

    for i in range(N):
        if i not in visited:
            count += 1
            visited.add(i)
            dfs(i)

    return count

class UnionFind(object):
    """并查集类"""
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        self.uf = [-1 for i in range(len(isConnected) + 1)]  # 列表0位置空出
        self.sets_count = len(isConnected)  # 判断并查集里共有几个集合, 初始化默认互相独立
        for i in range(len(isConnected)):
            for j in range(i, len(isConnected[i])):
                if i == j or isConnected[i][j] == 0:
                    continue
                else:
                    # print("union:", i, j)
                    self.union(i, j)

        # print(self.sets_count)
        # print(self.uf)
        return self.sets_count

    def find(self, p):
        """尾递归"""
        if self.uf[p] < 0:
            return p
        self.uf[p] = self.find(self.uf[p])
        return self.uf[p]

    def union(self, p, q):
        """连通p,q 让q指向p"""
        proot = self.find(p)
        qroot = self.find(q)
        if proot == qroot:
            return
        elif self.uf[proot] > self.uf[qroot]:   # 负数比较, 左边规模更小
            self.uf[qroot] += self.uf[proot]
            self.uf[proot] = qroot
        else:
            self.uf[proot] += self.uf[qroot]  # 规模相加
            self.uf[qroot] = proot
        self.sets_count -= 1                    # 连通后集合总数减一

    def is_connected(self, p, q):
        """判断pq是否已经连通"""
        return self.find(p) == self.find(q)     # 即判断两个结点是否是属于同一个祖先


def rotate(self, nums: List[int], k: int) -> None:
    n = len(nums)
    k = k % n
    if k == 0: return nums
    for i in range(k):
        last = nums[-1]
        for i in range(n -1, 0, -1):
            nums[i] = nums[i-1]
        nums[0] = last


def rotate2(self, nums: List[int], k: int) -> None:
    n = len(nums)
    k = k % n
    curv = nums[-1]
    curi = n - 1
    swap = curi - k
    for i in range(n-1):
        if curi - k < 0:
            swap = curi - k + 8
        else:
            swap = curi - k
        print(curi, swap)
        nums[curi] = nums[swap]
        curi = swap

    nums[curi] = curv

    print(nums)
    pass


def twoSum(self, nums: List[int], target: int) -> List[int]:
    """
    nums = [2,7,11,15]
    target = 9
    nums1 = [3, 2, 4]
    target1 = 6
    twoSum("", nums, target)
    """
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if i == j:
                continue
            if nums[i] + nums[j] == target:
                return [i, j]


    pass
if __name__ == '__main__':
    pass
    # n1 = [1,3]
    # n2 = [1,2]
    # mid = findMedianSortedArrays("", n1, n2)
    # print(mid)



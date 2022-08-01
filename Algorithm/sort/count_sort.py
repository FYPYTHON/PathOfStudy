# coding=utf-8
"""
array:[9,6,3,1]
count:[0,0,0,0,0,0,0,0,0,0]
count:1,3,6,9的位置值为1 :
      [0,1,0,1,0,0,1,0,0,1]
计算array中每个数小于的几个
      [0,1,1,2,2,2,3,3,3,4]
比9小的4个，6小的3个，3小的2个，1小的1个
"""
import random

+++++++++++++++

def countingSort(alist,k):
    n = len(alist)
    b = [0 for i in range(n)]
    c = [0 for i in range(k+1)]
    for i in alist:
        c[i] += 1
    print(c)
    for i in range(1, len(c)):
        c[i] = c[i-1]+c[i]
        print(c)
    for i in alist:
        b[c[i]-1] = i
        c[i] -= 1
    return b


if __name__=='__main__':
    a = [random.randint(0, 100) for i in range(10)]
    a = [9, 6, 3, 1]
    print(a)
    print(countingSort(a, 10))

# coding=utf-8


def combination_k(s, k):
    """
    s --> 输入的字符串
    k --> 选取的元素的个数
    combination_k('abc', 2) >>> ['ab', 'ac', 'bc']
    """
    # recursive basis
    if k == 0: return ['']
    # recursive chain
    subletters = []
    # 此处涉及到一个 python 遍历循环的特点：当遍历的对象为空（列表，字符串...）时，循环不会被执行，range(0) 也是一样
    for i in range(len(s)):
        print(i)
        result = combination_k(s[i+1:], k-1)
        print(result)
        for letter in result:
            subletters += [s[i] + letter]
            print("s:", subletters)
    return subletters


def get_arrs(num):
    a = [1, 2, 3, 4, 5, 6]
    lists = []
    for i in range(num):
        lists.append(a)
    return lists


def permutation_dice(lists, k):
    if k == 1:
        return lists
    all_perm = []

    result = permutation_dice(lists, k - 1)
    for item in result:
        for j in lists:
            all_perm += [str(j) + str(item)]
    return all_perm


def permutation2_dice(lists, k):
    if k == 1:
        return lists
    all_perm = []

    result = permutation2_dice(lists, k - 1)
    for item in result:
        for j in lists:
            if isinstance(item, list):
                all_perm += [item + [j]]
            else:
                all_perm += [[item] + [j]]
    return all_perm

def main():
    lists = [1,2,3,4,5,6]
    # res = permutation_dice(lists, 6)
    res = permutation2_dice(lists, 6)
    print(res)
    print(len(res))

def touzi6():
    nums = [1,2,3,4,5,6]
    res = []
    for i in range(111111, 666667):
        if '7' in str(i):
            continue
        elif '8' in str(i):
            continue
        elif '9' in str(i):
            continue
        elif '0' in str(i):
            continue
        else:
            res.append([int(j) for j in str(i)])
    return res


if __name__ == '__main__':
    # print(combination_k('abc', 2))
    main()
    import time
    t1 = time.time()
    res = touzi6()
    print(res)
    print(len(res))
    print(time.time()-t1)

# coding=utf-8

from functools import reduce


def lists_combination(lists, code=''):
    """
    输入多个列表组成的列表, 输出其中每个列表所有元素可能的所有排列组合
    code用于分隔每个元素
    :param lists: [[],[]]
    :param code: 分割符,
    :return:
    """
    try:
        import reduce
    except:
        from functools import reduce

    def myfunc(list1, list2):
        return [str(i) + code + str(j) for i in list1 for j in list2]

    return reduce(myfunc, lists)


def get_fn():
    """
    fn 俩俩相加
    :return:
    """
    fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
    return fn


def permutation_dice(lists, k):
    """
    6个骰子的全排列
    :param lists: [1,2,3,4,5,6] 一个骰子的所有值
    :param k:  骰子个数
    :return:
    """
    if k == 1:
        return lists
    all_perm = []

    result = permutation_dice(lists, k - 1)
    for item in result:
        for j in lists:
            all_perm += [str(j) + str(item)]
    return all_perm


def permutation2_dice(lists, k):
    """
    6个骰子的全排列
    :param lists: [1,2,3,4,5,6] 一个骰子的所有值
    :param k:  骰子个数
    :return:
    """
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


def touzi6():
    """
    枚举方式获取6个骰子全排列
    :return:
    """
    # nums = [1, 2, 3, 4, 5, 6]
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


def get_arrs(num):
    a = [1, 2, 3, 4, 5, 6]
    if num == 1:
        return a
    lists = []
    for i in range(num):
        lists.append(a)
    return lists


def all_perm(lists):
    """
    用 reduce 相加求全排列
    :param lists:
    :return:
    """
    func_perm = lambda x, code=',': reduce(lambda x, y: ['%s,%s' % (i, j) for i in x for j in y], x)
    lists = func_perm(lists)
    func_to_int = lambda x: [int(i) for i in x.split(',')]

    return [func_to_int(i) for i in lists]


def cal_freq(lists):
    """
    计算骰子的出现概率
    """
    freq_dict = dict()
    for i in range(len(lists)):
        temp = lists[i]
        key = sum(temp)
        if freq_dict.__contains__(key):
            freq_dict[key] += 1
        else:
            freq_dict[key] = 1
    return freq_dict


def get_max_freq(freq_dict):
    """
    计算骰子的最大概率
    """
    valuse = freq_dict.values()
    max_freq = max(list(valuse))
    print("max:", max_freq)
    res = [(k, v) for k, v in freq_dict.items() if v == max_freq]
    return res

def t_main():
    import time
    t1 = time.time()
    ori_lists = get_arrs(1)
    res_lists = permutation2_dice(ori_lists, 6)
    freq_res = cal_freq(res_lists)
    print(freq_res)
    max_res = get_max_freq(freq_res)
    print(max_res)
    print(time.time() - t1)

def main():
    import time
    t1 = time.time()
    ori_lists = get_arrs(6)
    res_lists = all_perm(ori_lists)
    freq_res = cal_freq(res_lists)
    print(freq_res)
    max_res = get_max_freq(freq_res)
    print(max_res)
    print(time.time() - t1)



if __name__ == "__main__":
    main()
    t_main()
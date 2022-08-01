#coding=utf-8
# 46 3 82 90 56 17 95

# 分裂
# [46 3 82] | [90 56 17 95]
# [46 3] [82] | [90 56] [17 95]
# [46] [3] [82] | [90] [56] [47] [95]

# 合并
# [46] [3] [82] | [90] [56] [47] [95]
# [3, 46] [82]  | [56,90] [47 95]
# [3,46,82]     | [47,56,90,95]
# [3,46,47,56,82,90,85]


def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)


def merge(left, right):
    l, r = 0, 0
    sort_list = []
    while l < len(left) and r < len(right):
        # print(left, right)
        if left[l] < right[r]:
            sort_list.append(left[l])
            l = l + 1
        else:
            sort_list.append(right[r])
            r = r + 1
    sort_list += left[l:]
    sort_list += right[r:]
    return sort_list

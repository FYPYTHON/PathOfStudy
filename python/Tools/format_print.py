# coding=utf-8
import sys
import os


title = ['location', 'ServiceName', 'Status', 'Role', 'IP', 'Port', 'Output']
data = [
    ['15fcb6e2-e31d', '数据中心机房', '正常', '主机', '192.168.2.8的', '9223',
     ' HTTP GET http://192.168.2.8:9200/role: 200 OK'],
    ['15fcb6e2-e31d', 'redis', '正常的', '主机', '192.168.2.8', '5686',
     ' Redis connect 192.168.2.8:5686: Success'],
    ['15fcb6e2-e31d', '资源a机房', '正常', '从机', '192.168.2.8', '5686',
     ' Redis connect 192.168.2.8:5686: Success'],
    ['1', '1', '异常', '从机', '5', '端口', ' 7']
]


def my_print():
    fmt_line = "+{}+".format("-" * 164)

    def get_length_with_ch(str):
        count = len(str.encode('gbk')) - len(str)
        return count

    def get_length_with_ch_linux(str):
        count = len(str.encode()) - len(str)
        return count // 2

    if not sys.platform.startswith("win"):  # linux
        size_list = [37, 13, 7, 7, 13, 5, 59]  # 用奇数
        fmt_data = "| {{:<{}}} | {{:<{}s}} | {{:<{}s}} | {{:<{}s}} | {{:<{}s}} | {{:<{}s}} | {{:<{}s}} |"
    else:  # win
        size_list = [38, 14, 8, 8, 14, 6, 60]  # 用偶数 + \t对齐
        fmt_data = "| {{:<{}}}\t | {{:<{}s}}\t | {{:<{}s}}\t | {{:<{}s}}\t | {{:<{}s}}\t | {{:<{}s}}\t | {{:<{}s}} |"

    print(fmt_line)
    print(fmt_data.format(*[str(i) for i in size_list]).format(*title))
    print(fmt_line)
    for d_info in data:
        if not sys.platform.startswith("win"):  # linux
            new_size_list = [a - b for (a, b) in zip(size_list, [get_length_with_ch_linux(d) for d in d_info])]
            print(fmt_data.format(*new_size_list).format(*d_info))
        else:  # win
            new_size_list = [a - b for (a, b) in zip(size_list, [get_length_with_ch(d) for d in d_info])]
            print(fmt_data.format(*new_size_list).format(*d_info))

    print(fmt_line)


def tabulate_lib():
    """
    pin install tabulate
    :return: 
    """
    from tabulate import tabulate

    # print(tabulate(data, headers=title, tablefmt='html', numalign='left', stralign='left'))  # use web api
    print(tabulate(data, headers=title, tablefmt='grid', numalign='left', stralign='left'))


if __name__ == '__main__':
    # tabulate_lib()
    my_print()


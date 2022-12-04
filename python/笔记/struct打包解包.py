# coding=utf-8
"""
struct模块

在Python中，『一切皆对象』，基本数据类型也不列外

C语言的数组int a[3] = {1, 2, 4};，存储的是真正的值
Python的列表lyst = [1, 2, 4]，存储的是元素的指针

这就造成了『列表元素的不连续存储』，在Python中列表中的数据可能不会被存储为连续的字节块

为了处理它们，将python值转换为C结构很重要，即将它们打包成连续的数据字节，或者将一个连续的字节块分解成Python对象

struct模块执行Python值和以Pythonbytes表示的C结构体之间的转换,这可以用于处理存储在文件中或来自网络连接以及其他源的二进制数据；它使用一定格式的字符串作为C语言结构布局的简洁描述以及到或从Python值的预期转换

fmt       c          python    标准尺寸
x
c         char        str        1
b      signed char    int        1
B     usigned char    int        1
?         _Bool       bool       1
h         short       int        2
H     usigned short   int        2
i         int         int        4
I     usigned int     int        4
l         long        int        4
L     usigned long    int        4
q        log log      int        8
Q  usigned long long  int        8
n         ssize_t     int
N          size_t     int
f         float       float       4
d         double      float       8
s         char[]      str
p         char[]      str
P         void*       int
"""

# struct模块最重要的两个函数就是pack()、unpack()方法
# 打包函数：pack(fmt, v1, v2, v3, ...)
# 解包函数：unpack(fmt, buffer)
import struct
dat1 = struct.pack('i', 2)
print(dat1)

s_data1 = struct.unpack('i', dat1)
print(s_data1)

dat2 = struct.pack('iii', 10, 23, 45)
d1, d2, d3 = struct.unpack('iii', dat2)
print(dat2, d1, d2, d3)
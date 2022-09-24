# coding=utf-8
# auth: 1823218990@qq.com
# time: 2021-09-24 13:12:10

import ctypes
from ctypes import c_char_p,c_int, create_string_buffer, POINTER, pointer, Structure
from ctypes import c_float, c_char, string_at, cast
SO_LIB = '/home/fy/pyc/cpplib/'
C_NULL = '\x00'
# export LD_LIBRARY_PATH="/home/testlib/testlib/:$LD_LIBRARY_PATH"
# source ~/.bashrc
# global_so = ctypes.CDLL(SO_LIB + 'global.so', mode=ctypes.RTLD_GLOBAL)


pyc_so = ctypes.CDLL(SO_LIB + 'libpyc.so')
print(pyc_so)
# char achKey[1024];
# char achValue[1024];
# int  nLen;


class KeyValue(Structure):
    _fields_ = [
        ('achKey', c_char * 1024),
        ('achValue', c_char * 1024),
        ('nLen', c_int)

    ]

class IdNum(Structure):
    _fields_ = [
        ('number', c_int),  # 576
        ('id', c_char_p),  # 64
    ]

def add():
    """
    int
    :return:  num1 + num2
    """
    num1 = c_int(2)
    num2 = c_int(2)

    pyc_so.add.restype = c_int
    pyc_so.add.argtypes = [POINTER(c_int), c_int]
    result = pyc_so.add(pointer(num1), num2)
    # print("result add:", num1.value, "+", num2.value)
    # print(result)


def sub():
    """
    float
    :return: num2- num1
    """
    num1 = c_float(3.0)
    num2 = c_float(4.0)
    pyc_so.sub.restype = c_float
    pyc_so.sub.argtypes = [POINTER(c_float), c_float]
    result = pyc_so.sub(pointer(num1), num2)
    # print("result sub:", num2.value, '-', num1.value)
    # print(result)

def GetKeyValue():
    kv = KeyValue()
    kv.achKey = b'tews'
    kv.achValue = b'valu1df'
    kv.nLen = 2
    pyc_so.GetKeyValue.restype = KeyValue
    pyc_so.GetKeyValue.argtypes = [KeyValue]
    result = pyc_so.GetKeyValue(kv)
    print("GetKeyValue:", result.achKey, result.achValue, result.nLen)
    # print("KeyValue:", kv)
    # print(kv.achKey, kv.achValue, kv.nLen)

def GetCPointer():
    pass
    idnum = IdNum()
    # idnum.id = create_string_buffer(C_NULL, 20)
    id_init = (C_NULL * 21).encode('utf-8')
    idnum.id = c_char_p(id_init)
    idnum.number = c_int(18)
    pyc_so.GetCPointer.restype = c_int
    pyc_so.GetCPointer.argtypes = [POINTER(IdNum)]
    result = pyc_so.GetCPointer(pointer(idnum))
    print("GetCPointer return:", result)
    print("IdNum:", string_at(idnum.id), idnum.number.value)

def GetCPointer1():
    pass
    idnum = IdNum()
    id_init = b'python c dll'
    
    idnum.id = c_char_p(id_init)
    idnum.number = c_int(18)
    size = c_int(21)
    pyc_so.GetCPointer1.restype = c_char_p
    pyc_so.GetCPointer1.argtypes = [POINTER(IdNum), c_int]
    result = pyc_so.GetCPointer1(pointer(idnum), size)
    print("GetCPointer1 return:", result)
    # print("IdNum.number:", result.number)
    # print("IdNum.id:", string_at(result.id))



if __name__ == '__main__':
    add()
    sub()

    GetKeyValue()
    # GetCPointer()

    GetCPointer1()
    # pyc_so.idaddr.restype = c_int
    # pyc_so.idaddr.argtypes = [IdAddr]   # POINTER(IdAddr) --> IdAddr*
    # pyc_so.idaddr(idaddr)

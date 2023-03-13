# coding=utf-8
"""
https://www.cnblogs.com/wztshine/p/15839038.html
nargs：ArgumentParser对象通常将一个动作与一个命令行参数关联。nargs关键字参数将一个动作与不同数目的命令行参数关联在一起：python xxx.py -v 1 2 3 这句代码中， -v 参数后面跟了3个值：1 2 3，这三个值都属于 -v ，我们就可以通过 nargs 定义一个参数后面可以跟随几个值。

nargs='?': 参数可以填0个或一个，解决：the following arguments are required: item

"""
import argparse
import sys
# python3 python_argparse.py -a -v y test.py
#   Namespace(abc=None, confirm='y', file='test.py', ver='ver')
# python3 python_argparse.py -a abc y test.py
#   Namespace(abc='abc', confirm='y', file='test.py', ver=None)
def argspares_test():
    parse = argparse.ArgumentParser(description="this is a test function!")
    parse.add_argument('-a','--abc',help='test args',nargs='?')
    parse.add_argument('-v','--ver',type=str,action='store_true')
    # action作用: xx.py -v (有-v则为true, -v不带参数)
    parse.add_argument('confirm',choices=('y','n'),default='y')
    parse.add_argument('file')
    print(sys.argv)
    args = parse.parse_args()
    print("argsparse:")
    # for ar in args:
    #     print("%s"%(ar))
    print(args.abc)
    print(args)

if __name__ == "__main__":
    argspares_test()

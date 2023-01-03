# coding=utf-8
import argparse
import sys
# python3 python_argparse.py -a -v y test.py
#   Namespace(abc=None, confirm='y', file='test.py', ver='ver')
# python3 python_argparse.py -a abc y test.py
#   Namespace(abc='abc', confirm='y', file='test.py', ver=None)
def argspares_test():
    parse = argparse.ArgumentParser(description="this is a test function!")
    parse.add_argument('-a','--abc',help='test args',nargs='?')
    parse.add_argument('-v','--ver',type=str,action='store')
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
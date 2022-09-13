# coding=utf-8
import configparser
import collections

# delimiters 定界符
configparser.ConfigParser.__init__(self, dict_type=collections.OrderedDict, delimiters=('='))
#coding=utf-8
"""
需要工具如下：
    pyinstaller：用于打包的工具软件
    png2ico:用于制作图标的工具
    upx：用于压缩，可以减小生成文件的大小

工具获取以及安装：
    pyinstaller：可以直接用python自带的pip的进行，主要注意pyinstaller的版本要和python的版本配套使用，
                否则生成可执行文件的时候会报错。我用的pyinstaller是3.2，python是2.7.12。安装完pyinstaller以后记得配置环境变量。
    png2ico:可以在[http://www.winterdrache.de/freeware/png2ico/]上获取，里面也有用法介绍，非常简单，不在多言。
    upx：在[http://upx.sourceforge.net/]可以获取到，甚至可以看到source code不得不感叹开源的强大啊。

安装命令：
     pyinstaller [PyUiFileCompare.py] -w -F --icon="name.ico" --upx-dir [upx_path]
     PyUiFileCompare.py: 可执行的main py文件
     upx_path：upx 所在路径,不能有中文目录
     icon: 程序图标
"""
from ui.mainwindow import *
import argparse, sys

parser = argparse.ArgumentParser(description="PyUiFileCompare - Tkinter GUI tool based on Python's difflib")
parser.add_argument('-p', '--paths', metavar=('path1', 'path2'), nargs=2, help='Two paths to compare', required=False)

args = parser.parse_args()

leftpath = args.paths[0] if args.paths else None
rightpath = args.paths[1] if args.paths else None
DEFAULT_PATH = 'C:\\workspace\\rother\\PyQt\\filecompare'
if __name__ =="__main__":
    ico = 'name.ico'
    # leftpath = C:\workSpace\rother\PyQt\filecompare
    main_window = MainWindow(leftpath, rightpath , ico=ico)
    # geometry('200x200+100+100')
    # main_window.main_window.iconbitmap(ico)
    # main_window.start(leftpath, rightpath , ico=ico)
    # main_window.start()
    main_window.main_window.mainloop()

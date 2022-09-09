# coding=utf-8
"""
author:
create:2019/6/5
"""
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./kafka_client.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s %(asctime)s]-[%(funcName)s]-[%(pathname)s %(lineno)s]: %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)
# logger.info("Start print log")
# logger.debug("Do something")
# logger.warning("Something maybe fail.")
# logger.info("Finish")
"""
需要工具如下：
    pyinstaller：用于打包的工具软件
    png2ico:用于制作图标的工具
    upx：用于压缩，可以减小生成文件的大小

工具获取以及安装：
    pyinstaller：可以直接用python自带的pip的进行，主要注意pyinstaller的版本要和python的版本配套使用，
                否则生成可执行文件的时候会报错。我用的pyinstaller是3.2，python是2.7.12。安装完pyinstaller以后记得配置环境变量。
    png2ico:可以在[http://www.winterdrache.de/freeware/png2ico/]上获取，里面也有用法介绍，非常简单，不在多言。
            png2ico favicon.ico logo16x16.png logo32x32.png
    upx：在[http://upx.sourceforge.net/]可以获取到，甚至可以看到source code不得不感叹开源的强大啊。

安装命令：
     pyinstaller [PyUiFileCompare.py] -w -F --icon="name.ico" --upx-dir [upx_path]
     PyUiFileCompare.py: 可执行的main py文件
     upx_path：upx 所在路径,不能有中文目录
     icon: 程序图标
     eg:
     python3 -m pip install -U --pre setuptools   # 升级setuptools库
     pyinstaller kafka_client/kafka_client.py -w -F --icon="kafka_client/kafka.ico" --upx-dir upx-3.95-win64/upx.exe
     or
     pyinstaller kafka_client.py -w -F --icon="kafka.ico" --upx-dir ../upx-3.95-win64/upx.exe

"""
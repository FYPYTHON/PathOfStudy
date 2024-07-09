* mycat使用 *

# 解压 mycat_1.6.tar.gz

目录如下：

drwxr-xr-x 2 root       root       4.0K  3月 28 18:08 bin
drwxrwxrwx 2 root       root       4.0K  3月  1  2016 catlet
drwxrwxrwx 4 root       root       4.0K  3月 28 18:34 conf
drwxr-xr-x 2 root       root       4.0K  3月 28 17:47 lib
drwxrwxrwx 2 root       root       4.0K  3月 28 19:07 logs
drwxr-xr-x 2 root       root       4.0K  3月 28 18:56 mysql_connect
-rwxrwxrwx 1 root       root        217 10月 28  2016 version.txt


# java 客户端

* mysql-connector-java-5.1.49-bin.jar 需要使用该版本 *

cd mysql_connect
sh test.sh


# mycat配置

替换配置文件
conf/server.xml
conf/schema.xml

# 启动
* 需要先导入java环境变量 *
./bin/mycat start

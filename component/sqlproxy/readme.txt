# https://blog.csdn.net/xiaojia1001/article/details/132516320
# https://blog.csdn.net/xiaojia1001/article/details/132516102

dm_flyway

# mysql-> dm不兼容的语法
1、sed -i "/use /d" ./*
   sed -i "/USE /d" ./*
2、sed -i "/SET NAMES utf8mb4/d" ./*/*
3、sed -i "/SET FOREIGN_KEY_CHECKS = 0/d" ./*/*
4、sed -i "/create database /d" ./*/*   
   sed -i "/CREATE database /d" ./*/*
5、sed -i "/ENGINE=InnoDB/d" ./*/*
6、sed -i "s/ENGINE = InnoDB//g" ./*/*

# pg-> dm不兼容
1、public -> user
2、int8 -> NUMBER
3、int4 -> integer
4、character varying -> VARCHAR2

# mysql -uUSER -ptestpwd1 -h127.0.0.1 -P9696 -Dap
# mysql -uUSER -ptestpwd1 -h172.16.237.8 -P9696 -Dmovision
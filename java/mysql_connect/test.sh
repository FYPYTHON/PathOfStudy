#!/bin/bash

# https://docs.oracle.com/javase/7/docs/technotes/tools/windows/java.html
# -classpath=-cp

javac -cp /home/wgq/java/mysql-connector-java-5.1.4-bin.jar TestDemo.java
java -cp $CLASSPATH:/home/wgq/java/mysql-connector-java-5.1.4-bin.jar TestDemo




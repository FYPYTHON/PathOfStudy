#!/bin/bash

mkdir ./jenkins

export JAVA_HOME=./jenkins/jdk-17.0.10
export CLASSPATH=$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin
export JRE_HOME=$JAVA_HOME/jre


export JENKINS_HOME=./jenkins/jks_home

mkdir -p ${JENKINS_HOME}



java -jar jenkins.war -Djava.awt.headless=true --httpPort=8080




ori_file=$1
des_file=$2


java -classpath /opt/midware/zookeeper/bin/../zookeeper-server/target/classes:/opt/midware/zookeeper/bin/../build/classes:/opt/midware/zookeeper/bin/../zookeeper-server/target/lib/*.jar:/opt/midware/zookeeper/bin/../build/lib/*.jar:/opt/midware/zookeeper/bin/../lib/zookeeper-jute-3.5.10.jar:/opt/midware/zookeeper/bin/../lib/zookeeper-3.5.10.jar:/opt/midware/zookeeper/bin/../lib/slf4j-reload4j-1.7.36.jar:/opt/midware/zookeeper/bin/../lib/slf4j-api-1.7.36.jar:/opt/midware/zookeeper/bin/../lib/reload4j-1.2.20.jar:/opt/midware/zookeeper/bin/../lib/netty-transport-native-unix-common-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-transport-native-epoll-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-transport-classes-epoll-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-transport-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-resolver-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-handler-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-common-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-codec-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/netty-buffer-4.1.77.Final.jar:/opt/midware/zookeeper/bin/../lib/json-simple-1.1.1.jar:/opt/midware/zookeeper/bin/../lib/jline-2.14.6.jar:/opt/midware/zookeeper/bin/../lib/jetty-util-ajax-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/jetty-util-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/jetty-servlet-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/jetty-server-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/jetty-security-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/jetty-io-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/jetty-http-9.4.46.v20220331.jar:/opt/midware/zookeeper/bin/../lib/javax.servlet-api-3.1.0.jar:/opt/midware/zookeeper/bin/../lib/jackson-databind-2.13.3.jar:/opt/midware/zookeeper/bin/../lib/jackson-core-2.13.3.jar:/opt/midware/zookeeper/bin/../lib/jackson-annotations-2.13.3.jar:/opt/midware/zookeeper/bin/../lib/commons-cli-1.2.jar:/opt/midware/zookeeper/bin/../lib/audience-annotations-0.5.0.jar:/opt/midware/zookeeper/bin/../zookeeper-*.jar:/opt/midware/zookeeper/bin/../zookeeper-server/src/main/resources/lib/*.jar:/opt/midware/zookeeper/bin/../conf::/usr/java/jdk1.8.0_221/lib:/usr/java/jdk1.8.0_221/lib/dt.jar:/usr/java/jdk1.8.0_221/lib/tools.jar org.apache.zookeeper.server.LogFormatter $1 1>$2

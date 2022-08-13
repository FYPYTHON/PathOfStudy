import org.apache.zookeeper.*;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.Watcher;

import java.io.IOException;

public class ZkClient {
    private static String hosts = "127.0.0.1:2183";
    private static int timeout = 30;
    private static ZooKeeper zk;
    private static String user = "test";
    private static String password = "zookeeper";

    private void init() throws IOException, KeeperException, InterruptedException {
        zk = new ZooKeeper(hosts, timeout, new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                System.out.println("go watch...");
                if(watchedEvent.getType() == Event.EventType.None && watchedEvent.getState() == Event.KeeperState.SyncConnected){
                    System.out.println("连接已经建立");
                }
            }
        });
    }

    public static void main(String[] args) throws IOException, KeeperException, InterruptedException {

        System.out.println("zkclient...");

        zk = new ZooKeeper(hosts, timeout, new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                System.out.println("go watch...");
                if(watchedEvent.getType() == Event.EventType.None && watchedEvent.getState() == Event.KeeperState.SyncConnected){
                    System.out.println("连接已经建立");
                }
            }
        });
        zk.addAuthInfo("digest", (user + ":" + password).getBytes());

        System.out.println("create...");

        String myNode = "/testData";

        if (zk.exists(myNode, false) != null){
            zk.delete(myNode, -1);
        }

        zk.create(myNode, "testData123".getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);

        byte[] data = zk.getData(myNode, false, null);
        System.out.println(new String(data));
        

    }
}

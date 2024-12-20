// package java_jdbc;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
public class jdbc_conn {
    static Connection con = null;
    static String cname = "dm.jdbc.driver.DmDriver";
    static String url = "jdbc:dm://localhost:5236";
    static String userid = "SYSDBA";
    static String pwd = "SYSDBA";
    public static void main(String[] args) {
        try {
            Class.forName(cname);
            con = DriverManager.getConnection(url, userid, pwd);
            con.setAutoCommit(true);
            System.out.println("[SUCCESS]conn database");
        } catch (Exception e) {
            System.out.println("[FAIL]conn database：" + e.getMessage());
        }
    }
    public void disConn(Connection con) throws SQLException {
        if (con != null) {
            con.close();
        }
    }
}



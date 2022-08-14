import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
public class TestDemo {
    // 定义 DM JDBC 驱动串
    static String jdbcString = "com.mysql.jdbc.Driver";
    // 定义 DM URL 连接串
    static String urlString = "jdbc:mysql://172.16.185.193:3320/www";
    // 定义连接用户名
    static String userName = "www";
    // 定义连接用户口令
    static String password = "www";
    // 定义连接对象
    static Connection conn = null;
    // 定义 SQL 语句执行对象
    static Statement state = null;
    // 定义结果集对象
    static ResultSet rs = null;
    public static void main(String[] args) {
        try {
            //1.加载 JDBC 驱动程序
            System.out.println("Loading JDBC Driver...");
            Class.forName(jdbcString);
            //2.连接 DM 数据库
            System.out.println("Connecting to DM Server...");
            conn = DriverManager.getConnection(urlString, userName, password);
            //3.通过连接对象创建 java.sql.Statement 对象
            state = conn.createStatement();
            //--------------------------------------------------------------------------------------------------
            //基础操作:此处操作对应的数据库,为示例库中的 BASECLOUD 模式中的 PRODUCT_CATEGORY 表
            //增加
            //定义增加的 SQL--这里由于此表中的结构为主键,自增,只需插入 name 列的值
            String sql_insert = "insert into PRODUCT_CATEGORY (id,name)values(1,'小说'),"+
                    "(2,'文学'),(3,'计算机'),(4,'英语'),(5,'管理'),(6,'少儿'),(7,'金融')";
            //执行添加的 SQL 语句
            System.out.println(sql_insert);
            state.executeUpdate(sql_insert);
            //删除
            //定义删除的 SQL 语句
            String sql_delete = "delete from PRODUCT_CATEGORY where name = '少儿'";
            //执行删除的 SQL 语句
            state.execute(sql_delete);
            //修改
            String sql_update = "update PRODUCT_CATEGORY set name = '国学' where name = '文学'";
            state.executeUpdate(sql_update);
            //查询表中数据
            //定义查询 SQL
            String sql_selectAll = "select * from PRODUCT_CATEGORY";
            //执行查询的 SQL 语句
            rs = state.executeQuery(sql_selectAll);
            displayResultSet(rs);
//---------------------------------------------------------------------------------------------------
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                //关闭资源
                rs.close();
                state.close();
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
    //显示结果集
    public static void displayResultSet(ResultSet rs) throws SQLException{
        while (rs.next()) {
            int i=1;
            Object id = rs.getObject(i++);
            Object name = rs.getObject(i++);
            System.out.println(id+"  "+name);
        }
    }
}
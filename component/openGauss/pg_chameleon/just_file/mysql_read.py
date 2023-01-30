# coding=utf-8
import os
import json
import decimal
from os import urandom
import multiprocessing
import pymysql
import MySQLdb
import MySQLdb.cursors
import codecs
from enum import Enum, unique

DEFAULT_MAX_SIZE_OF_CSV = 2 * 1024 * 1024
RANDOM_STR = "RANDOM_STR_SUFFIX"
MAX_EXECUTION_TIME = 9999000

def get_logger():
    # logger
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("./log_mysql_ch.log")
    fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
    console_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def token_hex(nbytes=16):
    return urandom(16).hex()


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


class Task():
    def __init__(self, destination_schema='meeting_bak', loading_schema='meeting', schema='meeting', table='test'):
        self.destination_schema = destination_schema
        self.loading_schema = loading_schema
        self.schema = schema
        self.table = table


class reader_cursor_manager(object):
    def __init__(self, conn_buffered, conn_unbuffered):
        self.cursor_buffered = conn_buffered.cursor()
        self.cursor_unbuffered = conn_unbuffered.cursor()

    def __del__(self):
        self.close()

    def close(self):
        self.cursor_buffered.close()
        self.cursor_unbuffered.close()

class ColumnType(Enum):
    """
        Some speical column type, pay attention to the enum prefix
    """
    # mysql data type
    M_HEX_BLOB = 'blob'
    M_HEX_T_BLOB = 'tinyblob'
    M_HEX_M_BLOB = 'mediumblob'
    M_HEX_L_BLOB = 'longblob'
    M_S_GIS_MUL_POINT = 'multipoint'
    M_S_GIS_MUL_LINESTR = 'multilinestring'
    M_S_GIS_MUL_POLYGON = 'multipolygon'
    M_S_GIS_GEOCOL = 'geometrycollection'
    M_S_GIS_GEOCOL2 = 'geomcollection'
    M_C_GIS_POINT = 'point'
    M_C_GIS_GEO = 'geometry'
    M_C_GIS_LINESTR = 'linestring'
    M_C_GIS_POLYGON = 'polygon'
    M_JSON = 'json'
    M_BINARY = 'binary'
    M_VARBINARY = 'varbinary'
    M_BIT = 'bit'
    M_DATATIME = 'datetime'
    M_TIMESTAMP = 'timestamp'
    M_DATE = 'date'
    M_INTEGER = 'integer'
    M_MINT = 'mediumint'
    M_TINT = 'tinyint'
    M_SINT = 'smallint'
    M_INT = 'int'
    M_BINT = 'bigint'
    M_VARCHAR = 'varchar'
    M_CHAR_VAR = 'character varying'
    M_TEXT = 'text'
    M_CHAR = 'char'
    M_TIME = 'time'
    M_TTEXT = 'tinytext'
    M_MTEXT = 'mediumtext'
    M_LTEXT = 'longtext'
    M_DECIMAL = 'decimal'
    M_DEC = 'dec'
    M_NUM = 'numeric'
    M_DOUBLE = 'double'
    M_DOUBLE_P = 'double precision'
    M_FLOAT = 'float'
    M_FLOAT4 = 'float4'
    M_FLOAT8 = 'float8'
    M_REAL = 'real'
    M_FIXED = 'fixed'
    M_YEAR = 'year'
    M_ENUM = 'enum'
    M_SET = 'set'
    M_BOOL = 'bool'
    M_BOOLEAN = 'boolean'
    #opengauss data type
    O_INTEGER = 'integer'
    O_BINT = 'bigint'
    O_TIMESTAP = 'timestamp'
    O_TIMESTAP_NO_TZ = 'timestamp without time zone'
    O_DATE = 'date'
    O_TIME = 'time'
    O_TIME_NO_TZ = 'time without time zone'
    O_BLOB = 'blob'
    O_BYTEA = 'bytea'
    O_BIT = 'bit'
    O_NUM = 'numeric'
    O_NUMBER = 'number'
    O_FLOAT = 'float'
    O_BIGSERIAL = 'bigserial'
    O_SERIAL = 'serial'
    O_DOUBLE_P = 'double precision'
    O_DEC = 'decimal'
    O_ENUM = 'enum'
    O_JSON = 'json'
    O_BOOLEAN = 'boolean'
    O_POINT = 'point'
    O_PATH = 'path'
    O_POLYGON = 'polygon'
    O_GEO = 'geometry'
    O_C_BPCHAR = 'bpchar'
    O_C_NCHAR = 'nchar'
    O_C_VARCHAR = 'varchar'
    O_C_VARCHAR2 = 'varchar2'
    O_C_NVCHAR2 = 'nvarchar2'
    O_C_CLOB = 'clob'
    O_C_CHAR = 'char'
    O_C_CHARACTER = 'character'
    O_C_CHAR_VAR = 'character varying'
    O_C_TEXT = 'text'
    O_SET = 'set'

    # @classmethod
    def __name_start_with(self, s):
        results = set()
        for k, v in ColumnType.__members__.items():
            if k.startswith(s):
                results.add(v.value)
        return results

    @classmethod
    def get_mysql_hexify_always_type(self):
        return ColumnType.__name_start_with('M_HEX_')

    @classmethod
    def get_mysql_postgis_spatial_type(self):
        return ColumnType.__name_start_with('M_S_GIS_')

    @classmethod
    def get_mysql_common_spatial_type(self):
        return ColumnType.__name_start_with('M_C_GIS_')

    @classmethod
    def get_opengauss_char_type(self):
        return ColumnType.__name_start_with('O_C_')

    @classmethod
    def get_opengauss_date_type(self):
        return {ColumnType.O_TIMESTAP.value, ColumnType.O_TIMESTAP_NO_TZ.value, ColumnType.O_DATE.value,
                ColumnType.O_TIME.value, ColumnType.O_TIME_NO_TZ.value}

    @classmethod
    def get_opengauss_hash_part_key_type(self):
        return {ColumnType.O_INTEGER.value, ColumnType.O_BINT.value, ColumnType.O_C_CHAR_VAR.value, ColumnType.O_C_TEXT.value,
            ColumnType.O_C_CHAR.value, ColumnType.O_NUM.value, ColumnType.O_NUMBER.value, ColumnType.O_DATE.value, ColumnType.O_TIME_NO_TZ.value,
            ColumnType.O_TIMESTAP_NO_TZ.value, ColumnType.O_TIME.value, ColumnType.O_TIMESTAP.value, ColumnType.O_C_BPCHAR.value,
            ColumnType.O_C_NCHAR.value, ColumnType.O_DEC.value}

class MysqlDBRead():
    def __init__(self, host='127.0.0.1', port=3320, user='test', password='test', schema='meeting', charset='utf8',
                 connect_timeout=30):
        self.port = port
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.schema = schema
        self.connect_timeout = connect_timeout
        self.conn_buffered = None
        self.schema_list = [schema]
        self.limit_tables = []
        self.skip_tables = []
        self.table_list = []
        #
        self.read_task_queue = multiprocessing.Manager().Queue()
        self.logger = get_logger()

        #
        self.hexify_always = ColumnType.get_mysql_hexify_always_type()
        self.hexify = self.hexify_always
        self.postgis_spatial_datatypes = ColumnType.get_mysql_postgis_spatial_type()
        self.common_spatial_datatypes = ColumnType.get_mysql_common_spatial_type()

        # temp data dir
        self.out_dir = "./data"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        if not os.path.exists(os.path.join(self.out_dir, self.schema)):
            os.makedirs(os.path.join(self.out_dir, self.schema))

    def get_connect(self, is_buffered=True):
        conn = MySQLdb.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            charset=self.charset,
            connect_timeout=self.connect_timeout,
            autocommit=True,
            cursorclass=MySQLdb.cursors.DictCursor if is_buffered else MySQLdb.cursors.SSCursor
        )
        return conn

    def connect_db_buffered(self):
        self.conn_buffered = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            charset=self.charset,
            connect_timeout=self.connect_timeout,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.charset = self.charset
        self.cursor_buffered = self.conn_buffered.cursor()

    def disconnect_db_buffered(self):
        try:
            self.conn_buffered.close()
        except:
            pass

    def connect_db_unbuffered(self):
        """
            The method creates a new connection to the mysql database.
            The connection is made using the unbuffered cursor factory.
        """
        self.conn_buffered = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            charset=self.charset,
            connect_timeout=self.connect_timeout,
            cursorclass=pymysql.cursors.SSCursor
        )
        self.charset = self.charset
        self.cursor_unbuffered = self.conn_unbuffered.cursor()

    def disconnect_db_unbuffered(self):
        try:
            self.conn_unbuffered.close()
        except:
            pass

    def gene_mysql_info(self):
        sql_log_bin = """SHOW GLOBAL VARIABLES LIKE 'version';"""
        self.cursor_buffered.execute(sql_log_bin)
        variable_check = self.cursor_buffered.fetchone()
        self.is_mariadb = False if variable_check["Value"].find(MARIADB) == -1 else True
        self.version = sql_token.parse_version(variable_check["Value"])
        mysql_version = -1 if self.is_mariadb is False else self.version
        self.logger.debug("mysql version %d" % self.version)
        with open(os.path.join(self.out_dir, "mysql.version")) as f:
            f.write(mysql_version)

    def lock_table(self, schema, table, cursor):
        self.logger.debug("locking the table `%s`.`%s`" % (schema, table))
        sql_lock = "FLUSH TABLES `%s`.`%s` WITH READ LOCK;" % (schema, table)
        cursor.execute(sql_lock)

    def unlock_tables(self, cursor):
        self.logger.debug("unlocking the tables")
        sql_unlock = "UNLOCK TABLES;"
        cursor.execute(sql_unlock)

    def get_master_coordinates(self, cursor_buffered=None):
        sql_master = "SHOW MASTER STATUS;"
        if cursor_buffered is None:
            self.cursor_buffered.execute(sql_master)
            master_status = self.cursor_buffered.fetchall()
        else:
            cursor_buffered.execute(sql_master)
            master_status = cursor_buffered.fetchall()
        return master_status

    def generate_select_statements(self, schema, table, cursor=None):

        random = token_hex(16) + RANDOM_STR
        select_columns = {}
        sql_select = """
            SELECT
                CASE
                    WHEN
                        data_type IN ('""" + "','".join(self.hexify) + """')
                    THEN
                        concat('hex(',column_name,')')
                    WHEN
                        data_type IN ('""" + ColumnType.M_BINARY.value + """')
                    THEN
                        concat('concat(\\'\\\\\\\\x\\', trim(trailing \\'00\\' from hex(',column_name,')))')
                    WHEN
                        data_type IN ('""" + ColumnType.M_BIT.value + """')
                    THEN
                        concat('cast(`',column_name,'` AS unsigned)')
                    WHEN
                        data_type IN ('""" + ColumnType.M_DATATIME.value + """','""" + ColumnType.M_TIMESTAMP.value + """','""" + ColumnType.M_DATE.value + """')
                    THEN
                        concat('nullif(`',column_name,'`,cast("0000-00-00 00:00:00" as date))')
                    WHEN
                        data_type IN ('""" + "','".join(self.postgis_spatial_datatypes) + """')
                    THEN
                        concat('ST_AsText(',column_name,')')
                    WHEN
                        data_type IN ('""" + ColumnType.M_C_GIS_POINT.value + """', '""" + ColumnType.M_C_GIS_GEO.value + """')
                    THEN
                        concat('SUBSTR(REPLACE(ST_AsText(',column_name,'),\\' \\',\\',\\'), 6)')
                    WHEN
                        data_type IN ('""" + ColumnType.M_C_GIS_POLYGON.value + """')
                    THEN
                        concat('SUBSTR(REPLACE(REPLACE(ST_AsText(',column_name,'),\\',\\',\\'),(\\'), \\' \\', \\',\\'),8)')
                    WHEN
                        data_type IN ('""" + ColumnType.M_C_GIS_LINESTR.value + """')
                    THEN
                        concat('concat(REPLACE(REPLACE(REPLACE(ST_AsText(',column_name,'),\\'LINESTRING\\',\\'[\\'),\\',\\',\\'),(\\'),\\' \\',\\',\\'),\\']\\')')

                ELSE
                    concat('cast(`',column_name,'` AS char CHARACTER SET """ + self.charset + """)')
                END
                AS select_csv,
                column_name as column_name
            FROM
                information_schema.COLUMNS
            WHERE
                table_schema=%s
                AND 	table_name=%s
            ORDER BY
                ordinal_position
            ;
        """
        if cursor is None:
            self.cursor_buffered.execute(sql_select, (schema, table))
            select_data = self.cursor_buffered.fetchall()
        else:
            cursor.execute(sql_select, (schema, table))
            select_data = cursor.fetchall()

        select_csv = "COALESCE(REPLACE(%s, '\"', '\"\"'),'{}') ".format(random)
        select_csv = [select_csv % statement["select_csv"] for statement in select_data]
        select_stat = [statement["select_csv"] for statement in select_data]
        column_list = ['"%s"' % statement["column_name"] for statement in select_data]
        select_columns["select_csv"] = "REPLACE(CONCAT('\"',CONCAT_WS('\",\"',%s),'\"'),'\"%s\"','NULL')" % (
        ','.join(select_csv), random)
        select_columns["select_stat"] = ','.join(select_stat)
        select_columns["column_list"] = ','.join(column_list)
        return select_columns

    # Use an inner class to represent transactions
    class reader_xact:
        def __init__(self, outer_obj, cursor, table_txs):
            self.outer_obj = outer_obj
            self.cursor = cursor
            self.table_txs = table_txs

        def __enter__(self):
            if self.table_txs:
                self.outer_obj.begin_tx(self.cursor)

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.table_txs:
                self.outer_obj.end_tx(self.cursor)
            else:
                self.outer_obj.unlock_tables(self.cursor)

    def begin_tx(self, cursor):
        self.logger.debug("set isolation level")
        cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
        self.logger.debug("beginning transaction")
        cursor.execute("BEGIN")

    def end_tx(self, cursor):
        self.logger.debug("rolling back")
        cursor.execute("ROLLBACK")

    def read_data_from_table(self, schema, table, cursor_manager):
        self.logger.debug("estimating rows in %s.%s" % (schema, table))
        sql_rows = """
            SELECT
                table_rows as table_rows,
                CASE
                    WHEN avg_row_length>0
                    then
                        round(({}/avg_row_length))
                ELSE
                    0
                END as copy_limit,
                transactions
            FROM
                information_schema.TABLES,
                information_schema.ENGINES
            WHERE
                    table_schema=%s
                AND	table_type='BASE TABLE'
                AND table_name=%s
                AND TABLES.engine = ENGINES.engine
            ;
        """
        cursor_buffered = cursor_manager.cursor_buffered
        cursor_unbuffered = cursor_manager.cursor_unbuffered
        sql_rows = sql_rows.format(DEFAULT_MAX_SIZE_OF_CSV)
        cursor_buffered.execute(sql_rows, (schema, table))
        count_rows = cursor_buffered.fetchone()
        total_rows = count_rows["table_rows"]
        copy_limit = int(count_rows["copy_limit"])
        table_txs = count_rows["transactions"] == "YES"
        if copy_limit == 0:
            copy_limit = 1000000
        num_slices = int(total_rows // copy_limit)
        range_slices = list(range(num_slices + 1))
        total_slices = len(range_slices)

        self.logger.debug(
            "The table %s.%s will be copied in %s  estimated slice(s) of %s rows, using a transaction %s" % (
            schema, table, total_slices, copy_limit, table_txs))

        # lock the table and flush the cache
        self.lock_table(schema, table, cursor_buffered)

        # get master status
        self.logger.debug("collecting the master's coordinates for table `%s`.`%s`" % (schema, table))
        # master_status = self.get_master_coordinates(cursor_buffered)
        master_status = ''

        select_columns = self.generate_select_statements(schema, table, cursor_buffered)
        sql_csv = "SELECT /*+ MAX_EXECUTION_TIME(%d) */ %s as data FROM `%s`.`%s`;" % \
                  (MAX_EXECUTION_TIME, select_columns["select_csv"], schema, table)
        self.logger.debug("Executing query for table %s.%s" % (schema, table))
        with self.reader_xact(self, cursor_buffered, table_txs):
            cursor_unbuffered.execute(sql_csv)
            # unlock tables
            if table_txs:
                self.unlock_tables(cursor_buffered)
            slice = 0
            while True:
                out_file = '%s/%s/%s_slice%d.csv' % (self.out_dir, schema, table, slice + 1)
                self.logger.info(out_file)
                csv_results = cursor_unbuffered.fetchmany(copy_limit)
                self.logger.info(len(csv_results))
                if len(csv_results) == 0:
                    break
                # '\x00' is '\0', which is a illeage char in openGauss, we need to remove it, but this
                # will lead to different value stored in MySQL and openGauss, we have no choice...
                csv_data = ("\n".join(d[0] for d in csv_results)).replace('\x00', '')

                csv_file = codecs.open(out_file, 'wb', self.charset)
                csv_file.write(csv_data)
                csv_file.close()
                # task = copy_data_task(out_file, count_rows, table, schema, select_columns, slice)
                task_file = os.path.join(self.out_dir, schema, ".task_{}_{}".format(table, slice))
                with open(task_file, 'w') as f:
                    # print(count_rows, select_columns, slice)
                    count_rows['copy_limit'] = str(count_rows['copy_limit'])
                    temp_dict = {"count_rows": count_rows, "select_columns": select_columns, "slice": slice}
                    f.write(json.dumps(temp_dict, cls=DecimalEncoder))
                slice += 1

        return master_status

    def __get_index_data(self, schema, table, cursor_buffered):
        sql_index = """
                    SELECT
                        index_name as index_name,
                        index_type as index_type,
                        non_unique as non_unique,
                        GROUP_CONCAT(column_name ORDER BY seq_in_index) as index_columns
                    FROM
                        information_schema.statistics
                    WHERE
                            table_schema=%s
                        AND 	table_name=%s
                        AND	(index_type = 'BTREE' OR index_type = 'FULLTEXT')
                    GROUP BY
                        table_name,
                        non_unique,
                        index_name,
                        index_type
                    ;
                """
        cursor_buffered.execute(sql_index, (schema, table))
        index_data = cursor_buffered.fetchall()
        return index_data

    def get_table_list(self):
        """
            The method pulls the table list from the information_schema.
            The list is stored in a dictionary  which key is the table's schema.
        """
        sql_tables="""
            SELECT
                table_name as table_name
            FROM
                information_schema.TABLES
            WHERE
                    table_type='BASE TABLE'
                AND table_schema=%s
            ;
        """
        self.connect_db_buffered()
        self.cursor_buffered.execute(sql_tables, (self.schema))
        table_list = [table["table_name"] for table in self.cursor_buffered.fetchall()]
        self.schema_tables = table_list
        return table_list

    def get_table_metadata(self, table, schema):
        """
            The method builds the table's metadata querying the information_schema.
            The data is returned as a dictionary.

            :param table: The table name
            :param schema: The table's schema
            :return: table's metadata as a cursor dictionary
            :rtype: dictionary
        """
        sql_metadata="""
            SELECT
                column_name as column_name,
                column_default as column_default,
                ordinal_position as ordinal_position,
                data_type as data_type,
                column_type as column_type,
                character_maximum_length as character_maximum_length,
                extra as extra,
                column_key as column_key,
                is_nullable as is_nullable,
                numeric_precision as numeric_precision,
                numeric_scale as numeric_scale,
                CASE
                    WHEN data_type="enum"
                THEN
                    SUBSTRING(COLUMN_TYPE,5)
                END AS enum_list,
                column_comment AS column_comment
            FROM
                information_schema.COLUMNS
            WHERE
                    table_schema=%s
                AND	table_name=%s
            ORDER BY
                ordinal_position
            ;
        """
        self.cursor_buffered.execute(sql_metadata, (schema, table))
        table_metadata = self.cursor_buffered.fetchall()
        return table_metadata

    def get_partition_metadata(self, table, schema):
        """
            The method builds the table's partition metadata querying the information_schema.
            The data is returned as a dictionary.

            :param table: The table name
            :param schema: The table's schema
            :return: table's partition metadata as a cursor dictionary
            :rtype: dictionary
        """
        sql_metadata="""
            SELECT DISTINCT
                partition_ordinal_position as partition_ordinal_position,
                subpartition_ordinal_position as subpartition_ordinal_position,
                subpartition_name as subpartition_name,
                subpartition_method as subpartition_method,
                subpartition_expression as subpartition_expression,
                partition_name as partition_name,
                partition_method as partition_method,
                partition_expression as partition_expression,
                partition_description as partition_description,
                tablespace_name as tablespace_name
            FROM
                information_schema.partitions
            WHERE
                    table_schema=%s
                AND table_name=%s
            ORDER BY
                partition_ordinal_position
            ;
        """
        self.cursor_buffered.execute(sql_metadata, (schema, table))
        partition_metadata = self.cursor_buffered.fetchall()
        return partition_metadata

    def create_destination_tables(self):
        """
            The method creates the destination tables in the loading schema.
            The tables names are looped using the values stored in the class dictionary schema_tables.
        """
        import json
        table_list = self.get_table_list()
        self.table_list = table_list
        tablelist_file = os.path.join(self.out_dir, self.schema, ".alltables")

        for table in table_list:
            table_metadata = self.get_table_metadata(table, self.schema)
            partition_metadata = self.get_partition_metadata(table, self.schema)
            # self.pg_engine.create_table(table_metadata, partition_metadata, table, schema, 'mysql')
            file_name = os.path.join(self.out_dir, self.schema, table)
            temp_dict = {
                "metadata_type": 'mysql',
                "schema": self.schema,
                "table": table,
                "table_metadata": table_metadata,
                "partition_metadata": partition_metadata
            }
            with open(file_name, 'w') as f:
                f.write(json.dumps(temp_dict))

            master_status = self.get_master_coordinates(self.cursor_buffered)
            indices = self.__get_index_data(schema=self.schema, table=table, cursor_buffered=self.cursor_buffered)
            # self.logger.info(indices)
            index_file = os.path.join(self.out_dir, self.schema, ".index_{}".format(table))
            temp_index_json = {
                "schema": self.schema,
                "table": table,
                "indices": indices,
                "master_status": master_status
            }
            with open(index_file, 'w') as f:
                f.write(json.dumps(temp_index_json))

        with open(tablelist_file, 'w') as f:
            f.write(json.dumps({"table_list": table_list}))


    def read_data_process(self, conn_buffered, conn_unbuffered, table):
        cursor_manager = reader_cursor_manager(conn_buffered, conn_unbuffered)
        destination_schema = self.schema
        loading_schema = self.schema
        schema = self.schema
        # table = task

        self.logger.info("Copying the source table %s into %s.%s" % (table, loading_schema, table))
        try:
            master_status = self.read_data_from_table(schema, table, cursor_manager)
            # indices = self.__get_index_data(schema=schema, table=table, cursor_buffered=cursor_manager.cursor_buffered)
            # self.logger.info(indices)
            # index_write_task = create_index_task(table, schema, indices, destination_schema, master_status)
            # self.index_waiting_queue.put(index_write_task, block=True)
        except:
            self.logger.info("Could not copy the table %s. Excluding it from the replica." % (table))
            raise
        finally:
            cursor_manager.close()

    def data_reader(self):
        self.create_destination_tables()
        for table in self.table_list:

            with self.get_connect(True) as conn_buffered, self.get_connect(False) as conn_unbuffered:
                # task = Task()
                self.read_data_process(conn_buffered, conn_unbuffered, table)

    def run(self):
        self.logger.info("run...")
        self.data_reader()


if __name__ == '__main__':
    pass
    user = 'kedacom'
    host = '172.16.80.191'
    port = 3320
    password = 'Keda!Mysql_36'
    sql_ch = MysqlDBRead(host=host, password=password, user=user, port=port)
    sql_ch.run()

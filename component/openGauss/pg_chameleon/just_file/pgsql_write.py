# coding=utf-8
import re
import datetime
import decimal
import io
import json
import multiprocessing as mp
import os
import sys
import time
import gc
import binascii
import py_opengauss
from enum import Enum, unique

my_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(my_path)
from sql_util import sql_token, ColumnType

# from MariaDB 10.2.7, Literals in the COLUMN_DEFAULT column in the Information Schema COLUMNS table
# are now quoted to distinguish them from expressions. https://mariadb.com/kb/en/mariadb-1027-release-notes/
COLUMNDEFAULT_INCLUDE_QUOTE_VER = 7 + sql_token.VERSION_SCALE * 2 + \
                                  (sql_token.VERSION_SCALE * sql_token.VERSION_SCALE) * 10


def get_logger():
    # logger
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("./log_pg_ch.log")
    fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
    console_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


class copy_data_task:
    def __init__(self, csv_file, count_rows, table, schema, select_columns, slice=0):
        self.csv_file = csv_file
        self.count_rows = count_rows
        self.table = table
        self.schema = schema
        self.select_columns = select_columns
        self.slice = slice


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
    # opengauss data type
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

    @classmethod
    def __name_start_with(self, s):
        results = set()
        for k, v in ColumnType.__members__.items():
            if k.startswith(s):
                results.add(v.value)
        return results

    @staticmethod
    def get_mysql_hexify_always_type():
        return ColumnType.__name_start_with('M_HEX_')

    @staticmethod
    def get_mysql_postgis_spatial_type():
        return ColumnType.__name_start_with('M_S_GIS_')

    @staticmethod
    def get_mysql_common_spatial_type():
        return ColumnType.__name_start_with('M_C_GIS_')

    @staticmethod
    def get_opengauss_char_type():
        return ColumnType.__name_start_with('O_C_')

    @staticmethod
    def get_opengauss_date_type():
        return {ColumnType.O_TIMESTAP.value, ColumnType.O_TIMESTAP_NO_TZ.value, ColumnType.O_DATE.value,
                ColumnType.O_TIME.value, ColumnType.O_TIME_NO_TZ.value}

    @staticmethod
    def get_opengauss_hash_part_key_type():
        return {ColumnType.O_INTEGER.value, ColumnType.O_BINT.value, ColumnType.O_C_CHAR_VAR.value,
                ColumnType.O_C_TEXT.value,
                ColumnType.O_C_CHAR.value, ColumnType.O_NUM.value, ColumnType.O_NUMBER.value, ColumnType.O_DATE.value,
                ColumnType.O_TIME_NO_TZ.value,
                ColumnType.O_TIMESTAP_NO_TZ.value, ColumnType.O_TIME.value, ColumnType.O_TIMESTAP.value,
                ColumnType.O_C_BPCHAR.value,
                ColumnType.O_C_NCHAR.value, ColumnType.O_DEC.value}


class pg_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.time) or \
                isinstance(obj, datetime.datetime) or \
                isinstance(obj, datetime.date) or \
                isinstance(obj, decimal.Decimal) or \
                isinstance(obj, datetime.timedelta) or \
                isinstance(obj, set) or \
                isinstance(obj, frozenset) or \
                isinstance(obj, bytes):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class pg_engine(object):
    def __init__(self, host='127.0.0.1', port=9242, user='test', password='test', schema='meeting_bak', charset='utf8',
                 connect_timeout=30):
        self.port = port
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.schema = schema
        self.source_schema = self.schema.strip("_bak")
        self.connect_timeout = connect_timeout
        self.migrate_default_value = True
        self.mysql_version = 5007003  # 10002007
        if sys.platform.startswith('win'):
            self.out_dir = ".\\data"
        else:
            self.out_dir = './data'
        self.logger = get_logger()
        # init pgsql connect
        self.pgsql_conn = self.connect_db()
        self.create_schema()
        ###
        self.table_ddl = {}
        self.idx_ddl = {}
        self.type_ddl = {}
        self.idx_sequence = 0
        self.type_dictionary = {
            ColumnType.M_INTEGER.value: ColumnType.O_INTEGER.value,
            ColumnType.M_MINT.value: ColumnType.O_INTEGER.value,
            ColumnType.M_TINT.value: ColumnType.O_INTEGER.value,
            ColumnType.M_SINT.value: ColumnType.O_INTEGER.value,
            ColumnType.M_INT.value: ColumnType.O_INTEGER.value,
            ColumnType.M_BINT.value: ColumnType.O_BINT.value,
            ColumnType.M_VARCHAR.value: ColumnType.O_C_CHAR_VAR.value,
            ColumnType.M_CHAR_VAR.value: ColumnType.O_C_CHAR_VAR.value,
            ColumnType.M_TEXT.value: ColumnType.O_C_TEXT.value,
            ColumnType.M_CHAR.value: ColumnType.O_C_CHARACTER.value,
            ColumnType.M_DATATIME.value: ColumnType.O_TIMESTAP_NO_TZ.value,
            ColumnType.M_DATE.value: ColumnType.O_DATE.value,
            ColumnType.M_TIME.value: ColumnType.O_TIME_NO_TZ.value,
            ColumnType.M_TIMESTAMP.value: ColumnType.O_TIMESTAP_NO_TZ.value,
            ColumnType.M_TTEXT.value: ColumnType.O_C_TEXT.value,
            ColumnType.M_MTEXT.value: ColumnType.O_C_TEXT.value,
            ColumnType.M_LTEXT.value: ColumnType.O_C_TEXT.value,
            ColumnType.M_HEX_T_BLOB.value: ColumnType.O_BLOB.value,
            ColumnType.M_HEX_M_BLOB.value: ColumnType.O_BLOB.value,
            ColumnType.M_HEX_L_BLOB.value: ColumnType.O_BLOB.value,
            ColumnType.M_HEX_BLOB.value: ColumnType.O_BLOB.value,
            ColumnType.M_BINARY.value: ColumnType.O_BYTEA.value,
            ColumnType.M_VARBINARY.value: ColumnType.O_BYTEA.value,
            ColumnType.M_DECIMAL.value: ColumnType.O_NUMBER.value,
            ColumnType.M_DEC.value: ColumnType.O_NUMBER.value,
            ColumnType.M_NUM.value: ColumnType.O_NUMBER.value,
            ColumnType.M_DOUBLE.value: ColumnType.O_NUMBER.value,
            ColumnType.M_DOUBLE_P.value: ColumnType.O_NUMBER.value,
            ColumnType.M_FLOAT.value: ColumnType.O_NUMBER.value,
            ColumnType.M_FLOAT4.value: ColumnType.O_NUMBER.value,
            ColumnType.M_FLOAT8.value: ColumnType.O_NUMBER.value,
            ColumnType.M_REAL.value: ColumnType.O_NUMBER.value,
            ColumnType.M_FIXED.value: ColumnType.O_NUMBER.value,
            ColumnType.M_BIT.value: ColumnType.O_INTEGER.value,
            ColumnType.M_YEAR.value: ColumnType.O_INTEGER.value,
            ColumnType.M_ENUM.value: ColumnType.O_ENUM.value,
            ColumnType.M_SET.value: ColumnType.O_SET.value,
            ColumnType.M_JSON.value: ColumnType.O_JSON.value,
            ColumnType.M_BOOL.value: ColumnType.O_BOOLEAN.value,
            ColumnType.M_BOOLEAN.value: ColumnType.O_BOOLEAN.value,
        }
        self.check_postgis()
        # args
        self.idx_sequence = 0
        self.max_range_column = 4
        self.hash_part_key_type = ColumnType.get_opengauss_hash_part_key_type()
        self.character_type = ColumnType.get_opengauss_char_type()
        self.date_type = ColumnType.get_opengauss_date_type()
        self.default_value_map = {
            # without time zone
            'curdate()': "CURRENT_DATE",
            'curtime()': "('now'::text)::time",
            'current_timestamp()': "pg_systimestamp()::timestamp",
            'current_timestamp': "pg_systimestamp()::timestamp",
            '0000-00-00 00:00:00': "NULL",
            '0000-00-00': "NULL"
        }
        for i in range(7):
            str = "current_timestamp(%s)" % i
            self.default_value_map[str] = str

        self.type_override = {
            "tinyint(1)":
                {
                    "override_to": "boolean",
                    "override_tables": ['*']
                }
        }

    def connect_db(self):
        strconn = "opengauss://%(host)s:%(port)s/%(database)s" % {'host': self.host, 'port': self.port,
                                                                  'database': self.schema}
        self.logger.info(strconn)
        pgsql_conn = py_opengauss.open(strconn, user=self.user, password=self.password, sslmode="disable")
        pgsql_conn.settings['client_encoding'] = self.charset
        pgsql_conn.execute("set session_timeout = 0;")
        self.logger.info("{}".format(pgsql_conn))
        return pgsql_conn

    def disconnect_db(self, pgsql_conn):
        if pgsql_conn:
            pgsql_conn.close()
            pgsql_conn = None

    def create_schema(self):
        self.pgsql_conn.execute("DROP SCHEMA IF EXISTS {} cascade;".format(self.schema))
        self.pgsql_conn.execute("CREATE SCHEMA {};".format(self.schema))

    def check_postgis(self):
        """
            The method checks whether postgis is present or not on the
        """
        sql_check = """
            SELECT
                count(*)=1
            FROM
                pg_extension
            WHERE
                extname='postgis';
        ;"""
        self.connect_db()
        stmt = self.pgsql_conn.prepare(sql_check)
        postgis_check = stmt.first()
        self.postgis_present = postgis_check
        if self.postgis_present:
            spatial_data = {
                ColumnType.M_C_GIS_GEO.value: ColumnType.O_GEO.value,
                ColumnType.M_C_GIS_POINT.value: ColumnType.O_GEO.value,
                ColumnType.M_C_GIS_LINESTR.value: ColumnType.O_GEO.value,
                ColumnType.M_C_GIS_POLYGON.value: ColumnType.O_GEO.value,
                ColumnType.M_S_GIS_MUL_POINT.value: ColumnType.O_GEO.value,
                ColumnType.M_S_GIS_GEOCOL.value: ColumnType.O_GEO.value,
                ColumnType.M_S_GIS_GEOCOL2.value: ColumnType.O_GEO.value,
                ColumnType.M_S_GIS_MUL_LINESTR.value: ColumnType.O_GEO.value,
                ColumnType.M_S_GIS_MUL_POLYGON.value: ColumnType.O_GEO.value
            }
        else:
            spatial_data = {
                ColumnType.M_C_GIS_GEO.value: ColumnType.O_POINT.value,
                ColumnType.M_C_GIS_POINT.value: ColumnType.O_POINT.value,
                ColumnType.M_C_GIS_LINESTR.value: ColumnType.O_PATH.value,
                ColumnType.M_C_GIS_POLYGON.value: ColumnType.O_POLYGON.value,
                ColumnType.M_S_GIS_MUL_POINT.value: ColumnType.O_BYTEA.value,
                ColumnType.M_S_GIS_GEOCOL.value: ColumnType.O_BYTEA.value,
                ColumnType.M_S_GIS_GEOCOL2.value: ColumnType.O_BYTEA.value,
                ColumnType.M_S_GIS_MUL_LINESTR.value: ColumnType.O_BYTEA.value,
                ColumnType.M_S_GIS_MUL_POLYGON.value: ColumnType.O_BYTEA.value
            }
        self.type_dictionary.update(spatial_data.items())
        return postgis_check

    def get_data_type(self, column, schema, table):
        if self.type_override:
            try:
                table_full = "%s.%s" % (schema, table)
                type_override = self.type_override[column["column_type"]]
                override_to = type_override["override_to"]
                override_tables = type_override["override_tables"]
                if override_tables[0] == '*' or table_full in override_tables:
                    column_type = override_to
                else:
                    column_type = self.type_dictionary[column["data_type"]]
                    # print("1", column["data_type"], self.type_dictionary[column["data_type"]])
            except KeyError:
                # print("2", column["data_type"], self.type_dictionary[column["data_type"]])
                column_type = self.type_dictionary[column["data_type"]]
        else:
            column_type = self.type_dictionary[column["data_type"]]
        return column_type

    def __trans_default_value(self, origin_default, column_type):
        if self.migrate_default_value is False or origin_default is None or origin_default == "NULL":
            return ''

        # print("character_type", self.character_type, "-", column_type)
        re_symbol = 'E' if column_type in self.character_type else ''
        # for mysql, mysql_version will be -1 which need to be quoted
        # for mariadb, mysql_version will be the real version num, need to be quoted when version < 10.2.7
        # when we need to quote value, we also need to add '\' to escape single quotation mark for string type
        quote = ''
        if self.mysql_version < COLUMNDEFAULT_INCLUDE_QUOTE_VER:
            if column_type in self.character_type:
                quote = '\''
                origin_default = origin_default.replace('\'', '\\\'')
            elif column_type in self.date_type:
                if origin_default.lower() in self.default_value_map:
                    origin_default = self.default_value_map.get(origin_default.lower())
                else:
                    quote = '\''
            else:
                pass
        else:
            origin_default = self.default_value_map.get(origin_default.lower(), origin_default)
        default_str = "DEFAULT %s%s%s%s" % (re_symbol, quote, origin_default, quote)
        return default_str

    def metadata_method_check(self, metadata, check_method):
        method_ck = metadata[0][check_method].upper()
        if method_ck == "RANGE" or \
                method_ck == "RANGE COLUMNS":
            return "RANGE"
        elif method_ck == "LIST" or \
                method_ck == "LIST COLUMNS":
            return "LIST"
        elif method_ck == "HASH" or method_ck == "KEY" or \
                method_ck == "LINEAR KEY" or \
                method_ck == "LINEAR HASH":
            return "HASH"
        else:
            return False

    def build_sub_partition(self, schema, table_name, sub_table_metadata, sub_partition_metadata):
        """
        This function is used to compile DDL statements that generate child partitions
        Range-Range, Range-List, Range-Hash
        List-Range, List-List, List-Hash
        Hash-Range, Hash-List, Hash-Hash
        """
        part_key = sub_partition_metadata[0]["partition_expression"].replace('`', '')
        part_key_split = part_key.split(',')
        sub_part_key = sub_partition_metadata[0]["subpartition_expression"].replace('`', '')
        if part_key == sub_part_key:
            print(
                "OpenGauss databases don't support that the partition and subpartition have the same partition key for the level-two partition tables, online migration won't migrate this scenario.")
            return ""

        if len(part_key_split) > self.max_range_column or \
                (sub_partition_metadata[0]["partition_method"] != "RANGE COLUMNS" and len(part_key_split) > 1):
            self.logger.warning("%s.%s's partition key num(%d) exceed max value, create as normal table" \
                                % (schema, table_name, len(part_key_split)))
            return ""

        # special case for KEY partition
        # but KEY is not support in subpartition
        if sub_partition_metadata[0]["partition_method"] == "KEY" or sub_partition_metadata[0][
            "partition_method"] == "LINEAR KEY":
            return ""

        # ok, let's make the partition clause
        partition_method = ") PARTITION BY "
        method = self.metadata_method_check(sub_partition_metadata, "partition_method")
        if not method:
            self.logger.warning("Unknown partition type: %s, create this table(%s.%s) as non-part table" \
                                % (sub_partition_metadata[0]["partition_method"], schema, table_name))
            return ""
        else:
            partition_method += method

        # and make the subpartition clause
        partition_method += "(" + part_key + ") SUBPARTITION BY "
        method = self.metadata_method_check(sub_partition_metadata, "subpartition_method")
        if not method:
            self.logger.warning("Unknown partition type: %s, create this table(%s.%s) as non-part table" \
                                % (sub_partition_metadata[0]["subpartition_method"], schema, table_name))
            return ""
        else:
            partition_method += method
        partition_method += "(" + sub_part_key + ") ("

        part_pcolumn = []
        part_scolumn = []
        part_p = ""
        part_s = ""
        for part_data in sub_partition_metadata:
            # partition
            if part_data["subpartition_ordinal_position"] == 1:
                if part_data["partition_method"] == "RANGE" or part_data["partition_method"] == "RANGE COLUMNS":
                    part_p = ' PARTITION %s VALUES LESS THAN (%s) ' % (
                    part_data["partition_name"], part_data["partition_description"])
                elif part_data["partition_method"] == "LIST" or part_data["partition_method"] == "LIST COLUMNS":
                    part_p = ' partition %s values(%s) ' % (
                    part_data["partition_name"], part_data["partition_description"])
                elif part_data["partition_method"] == "HASH" or part_data["partition_method"] == "LINEAR HASH":
                    part_p = ' partition %s ' % (part_data["partition_name"])
                else:
                    self.logger.warning("Unknown partition type: %s, create this table(%s) as non-part table" \
                                        % (sub_partition_metadata[0]["partition_method"], table_name))
                    return ""
                if part_data["tablespace_name"] != "" and part_data["tablespace_name"] != None:
                    part_p += " TABLESPACE %s " % (part_data["tablespace_name"])
                part_pcolumn.append(part_p)
                part_scolumn = []
            # subpartition
            part_s = " SUBPARTITION %s " % (part_data["subpartition_name"])
            if part_data["tablespace_name"] != "" and part_data["tablespace_name"] != None:
                part_s += " TABLESPACE %s " % (part_data["tablespace_name"])
            part_scolumn.append(part_s)
            def_part_c = str(',').join(part_scolumn)
            part_pcolumn.pop()
            part_pcolumn.append(part_p + " (" + def_part_c + " )")
        def_part = str(',').join(part_pcolumn)
        return partition_method + def_part

    def __check_part_key_datatype(self, table_metadata, part_key, table_name, schema):
        for key in part_key:
            for column in table_metadata:
                if (key.lower() == column["column_name"].lower()):
                    column_type = self.get_data_type(column, schema, table_name)
                    if column_type not in self.hash_part_key_type:
                        self.logger.warning("%s.%s.%s can't be used as a partition key, column type: %s" \
                                            % (schema, table_name, key, column_type))
                        return False
        return True

    def __build_create_table_mysql(self, table_metadata, partition_metadata, table_name, schema, temporary_schema=True):
        """
            The method builds the create table statement with any enumeration associated using the mysql's metadata.
            The returned value is a dictionary with the optional enumeration's ddl and the create table without indices or primary keys.
            on the destination schema specified by destination_schema.
            The method assumes there is a database connection active.

            :param table_metadata: the column dictionary extracted from the source's information_schema or builty by the sql_parser class
            :param table_name: the table name
            :param destination_schema: the schema where the table belongs
            :return: a dictionary with the optional create statements for enumerations and the create table
            :rtype: dictionary
        """

        destination_schema = schema

        column_comments = ''
        ddl_head = 'CREATE TABLE "%s"."%s" (' % (destination_schema, table_name)
        ddl_tail = ");"
        ddl_columns = []
        ddl_enum = []
        table_ddl = {}
        for column in table_metadata:
            if column["is_nullable"] == "NO":
                col_is_null = "NOT NULL"
            else:
                col_is_null = "NULL"
            column_type = self.get_data_type(column, schema, table_name)
            # print(column_type)
            # print(column)
            default_value = self.__trans_default_value(column.get("column_default"), column_type)
            # print(default_value)
            if 'default' in column.keys():
                if default_value == "" and column["default"] is not None and column["default"] != "":
                    default_value = " default %s " % (column["default"])
            # print(default_value)
            if column_type == "enum":
                enum_type = '"%s"."enum_%s_%s"' % (destination_schema, table_name[0:20], column["column_name"][0:20])
                sql_drop_enum = 'DROP TYPE IF EXISTS %s CASCADE;' % enum_type
                sql_create_enum = 'CREATE TYPE %s AS ENUM %s;' % (enum_type, column["enum_list"])
                ddl_enum.append(sql_drop_enum)
                ddl_enum.append(sql_create_enum)
                column_type = enum_type
            if column_type == "set":
                column_type = column["column_type"]
            if (column_type == ColumnType.O_C_CHAR_VAR.value or column_type == ColumnType.O_C_CHARACTER.value) and \
                    int(column["character_maximum_length"]) > 0:
                column_type = "%s (%s)" % (column_type, str(column["character_maximum_length"]))
            if column_type == ColumnType.O_NUM.value and ('numeric_scale' in column.keys()) and str(
                    column["numeric_scale"]) != "None":
                column_type = "%s (%s,%s)" % (
                    column_type, str(column["numeric_precision"]), str(column["numeric_scale"]))
            if column_type == ColumnType.O_NUMBER.value and ('numeric_scale' in column.keys()) and str(
                    column["numeric_scale"]) != "None":
                column_type = "%s (%s,%s)" % (
                    column_type, str(column["numeric_precision"]), str(column["numeric_scale"]))
            if column["extra"] == "auto_increment":
                if (column_type == ColumnType.O_INTEGER.value):
                    column_type = ColumnType.O_SERIAL.value
                else:
                    column_type = ColumnType.O_BIGSERIAL.value

            ddl_columns.append(' "%s" %s %s %s   ' % (column["column_name"], column_type, default_value, col_is_null))

            if "column_comment" in column and column["column_comment"] != "":
                column_comments = column_comments + ('comment on column "%s"."%s"."%s" is \'%s\';\n' \
                                                     % (destination_schema, table_name, column["column_name"],
                                                        column["column_comment"]))

        table_ddl["column_comments"] = column_comments
        def_columns = str(',').join(ddl_columns)
        table_ddl["enum"] = ddl_enum
        table_ddl["composite"] = []

        # non partition table or subpartition table, ignore partition_metadata
        if partition_metadata is None or len(partition_metadata) == 0 or partition_metadata[0][
            "partition_method"] is None:
            table_ddl["table"] = (ddl_head + def_columns + ddl_tail)
            return table_ddl

        if partition_metadata[0]["subpartition_method"] is not None:
            if partition_metadata[0]["subpartition_method"] == "":
                self.logger.warning("%s.%s is a composite partition table, ignore subpartition" % (schema, table_name))
            # now we get the subpartition part
            else:
                subpartition_method = self.build_sub_partition(schema, table_name, table_metadata, partition_metadata)
                if subpartition_method == "":
                    return ""
                table_ddl["table"] = (ddl_head + def_columns + subpartition_method + ddl_tail)
                return table_ddl

        # get partition key num
        part_key = partition_metadata[0]["partition_expression"].replace('`', '')
        part_key_split = part_key.split(',')

        if len(part_key_split) > self.max_range_column or \
                (partition_metadata[0]["partition_method"] != "RANGE COLUMNS" and len(part_key_split) > 1):
            self.logger.warning("%s.%s's partition key num(%d) exceed max value, create as normal table" \
                                % (schema, table_name, len(part_key_split)))
            table_ddl["table"] = (ddl_head + def_columns + ddl_tail)
            return table_ddl

        # special case for KEY partition
        if partition_metadata[0]["partition_method"] == "KEY" or partition_metadata[0][
            "partition_method"] == "LINEAR KEY":
            if self.__check_part_key_datatype(table_metadata, part_key_split, table_name, schema) == False:
                table_ddl["table"] = (ddl_head + def_columns + ddl_tail)
                return table_ddl

        # ok, let's make the partition clause
        partition_method = ") PARTITION BY "
        method = self.metadata_method_check(partition_metadata, "partition_method")
        if not method:
            self.logger.warning("Unknown partition type: %s, create this table(%s.%s) as non-part table" \
                                % (partition_metadata[0]["partition_method"], schema, table_name))
            table_ddl["table"] = (ddl_head + def_columns + ddl_tail)
            return table_ddl
        else:
            partition_method += method

        partition_method += "(" + part_key + ") ("
        part_column = []
        for part_data in partition_metadata:
            if partition_metadata[0]["partition_method"] == "RANGE" or \
                    partition_metadata[0]["partition_method"] == "RANGE COLUMNS":
                part_column.append(' partition %s values less than(%s) ' % (
                    part_data["partition_name"], part_data["partition_description"]))
            elif partition_metadata[0]["partition_method"] == "LIST" or \
                    partition_metadata[0]["partition_method"] == "LIST COLUMNS":
                part_column.append(
                    ' partition %s values(%s) ' % (part_data["partition_name"], part_data["partition_description"]))
            elif part_data["partition_method"] == "HASH" or part_data["partition_method"] == "KEY" or \
                    part_data["partition_method"] == "LINEAR KEY" or part_data["partition_method"] == "LINEAR HASH":
                part_column.append(' partition %s ' % (part_data["partition_name"]))
            else:
                self.logger.warning("Unknown partition type: %s, create this table(%s) as non-part table" \
                                    % (partition_metadata[0]["partition_method"], table_name))
                table_ddl["table"] = (ddl_head + def_columns + ddl_tail)
                return table_ddl

        def_part = str(',').join(part_column)
        table_ddl["table"] = (ddl_head + def_columns + partition_method + def_part + ddl_tail)
        return table_ddl

    def get_table_list(self):
        tablelist_file = os.path.join(self.out_dir, self.source_schema, ".alltables")
        if not os.path.exists(os.path.dirname(tablelist_file)):
            self.logger.error("{} not exist".format(tablelist_file))
            return
        with open(tablelist_file, 'r') as f:
            table_list_json = json.load(f)
        self.table_list = table_list_json['table_list']
        self.schema_tables = self.table_list

    def create_table(self, table_name):
        schema = self.schema
        file_name = os.path.join(self.out_dir, self.source_schema, table_name)
        if not os.path.exists(file_name):
            self.logger.error("{} not exist".format(file_name))
            return
        with open(file_name, 'r') as f:
            table_metadata_json = json.load(f)
        # temp_dict = {
        #     "schema": self.schema,
        #     "table": table,
        #     "table_metadata": table_metadata,
        #     "partition_metadata": partition_metadata
        # }
        metadata_type = table_metadata_json['metadata_type']
        table_metadata = table_metadata_json['table_metadata']
        partition_metadata = table_metadata_json['partition_metadata']

        table_ddl = {}  ####
        if metadata_type == 'mysql':
            table_ddl = self.__build_create_table_mysql(table_metadata, partition_metadata, table_name, schema)
        elif metadata_type == 'pgsql':
            table_ddl = self.__build_create_table_pgsql(table_metadata, table_name, schema)
        enum_ddl = table_ddl["enum"]
        composite_ddl = table_ddl["composite"]
        column_comments_ddl = (table_ddl["column_comments"] if "column_comments" in table_ddl else '')
        table_ddl = table_ddl["table"]

        for enum_statement in enum_ddl:
            self.pgsql_conn.execute(enum_statement)

        for composite_statement in composite_ddl:
            self.pgsql_conn.execute(composite_statement)

        # self.logger.info(table_ddl)
        self.pgsql_conn.execute(table_ddl)

        if column_comments_ddl != '':
            self.pgsql_conn.execute(column_comments_ddl)

    def _create_indices(self, schema, table, index_data):
        # print("index data:", schema, index_data)
        idx_ddl = {}
        table_primary = []
        for index in index_data:
            table_timestamp = str(int(time.time()))
            indx = index["index_name"]
            self.logger.debug("Building DDL for index %s" % (indx))
            idx_col = [column.strip() for column in index["index_columns"].split(',')]
            index_columns = ['"%s"' % column.strip() for column in idx_col]
            non_unique = index["non_unique"]
            index_type = index["index_type"]
            if indx == 'PRIMARY':
                pkey_name = format("pk_%s_%s_%s" % (table[0:100], table_timestamp, self.idx_sequence))
                pkey_def = 'ALTER TABLE "%s"."%s" ADD CONSTRAINT "%s" PRIMARY KEY (%s) ;' % (
                schema, table, pkey_name, ','.join(index_columns))
                idx_ddl[pkey_name] = pkey_def
                table_primary = idx_col
            else:
                if non_unique == 0:
                    unique_key = 'UNIQUE'
                    if table_primary == []:
                        table_primary = idx_col
                else:
                    unique_key = ''
                # openGauss doesn't support multi column for GIN index, so use BTREE when columns > 1
                if index_type == 'BTREE' or len(index_columns) > 1:
                    using = 'USING BTREE(%s)' % (','.join(index_columns))
                else:
                    using = "USING GIN(to_tsvector('simple', %s))" % (index_columns[0])
                index_name = 'idx_%s_%s_%s_%s' % (indx[0:10], table[0:10], table_timestamp, self.idx_sequence)
                idx_def = 'CREATE %s INDEX "%s" ON "%s"."%s" %s;' % (unique_key, index_name, schema, table, using)
                idx_ddl[index_name] = idx_def
            self.idx_sequence += 1

        for index in idx_ddl:
            self.logger.info("Building index %s on %s.%s" % (index, schema, table))
            self.pgsql_conn.execute(idx_ddl[index])

        return table_primary

    def create_index_process(self, table):
        index_file = os.path.join(self.out_dir, self.source_schema, ".index_{}".format(table))
        if not os.path.exists(index_file):
            self.logger.error("{} not exist".format(index_file))
            return
        # temp_index_json = {
        #     "schema": self.schema,
        #     "table": table,
        #     "indices": indices,
        #     "master_status": master_status
        # }
        with open(index_file, 'r') as f:
            temp_index_json = json.load(f)
        indices = temp_index_json['indices']
        master_status = temp_index_json['master_status']

        if indices is None:
            self.logger.error("index data is None")
            return
        if len(indices) == 0:
            self.logger.info("there are no indices be created, just store the table")
            # self.pgsql_conn.store_table(self.schema, table, [], master_status)
            return

        destination_schema = self.schema
        loading_schema = self.schema
        try:

            table_pkey = self._create_indices(loading_schema, table, indices)
            # self.pgsql_conn.store_table(destination_schema, table, table_pkey, master_status)
        except Exception as e:
            self.logger.error("create index or constraint error, {}".format(e))

    def print_progress(self, iteration, total, schema, table):
        if iteration >= total:
            total = iteration
        if total > 1:
            self.logger.info("Table %s.%s copied %s slice of %s" % (schema, table, iteration, total))
        else:
            self.logger.debug("Table %s.%s copied %s slice of %s" % (schema, table, iteration, total))

    def copy_table_data(self, table, csv_file_name, writer_engine):
        slice_insert = []

        csv_file = open(csv_file_name, 'rb')

        if csv_file is None:
            self.logger.warning("this is an empty csv file, you should check your batch for errors")
            return

        task_file = os.path.join(self.out_dir, self.source_schema, ".task_".format(os.path.basename(csv_file_name)))
        with open(task_file, 'r') as f:
            temp_dict = json.load(f)

        select_columns = temp_dict['select_columns']
        slice = temp_dict['slice']
        column_list = select_columns["column_list"]

        count_rows = temp_dict['count_rows']
        schema = self.schema
        total_rows = count_rows["table_rows"]
        copy_limit = int(count_rows["copy_limit"])
        loading_schema = self.schema

        if copy_limit == 0:
            copy_limit = 1000000
        num_slices = int(total_rows // copy_limit)
        range_slices = list(range(num_slices + 1))
        total_slices = len(range_slices)

        try:
            writer_engine.copy_data(csv_file, self.schema, table, column_list)
        except Exception as e:
            self.logger.error("SQLCODE: %s SQLERROR: %s" % (e.code, e.message))
            self.logger.info(
                "Table %s.%s error in PostgreSQL copy, saving slice number for the fallback to insert statements" % (
                    loading_schema, table))
            slice_insert.append(slice)
        finally:
            csv_file.close()
            try:
                # remove(csv_file)
                pass
            except:
                pass
            del csv_file

            gc.collect()
        self.print_progress(slice + 1, total_slices, schema, table)
        slice += 1

    def run(self):
        self.logger.info("mysql_version: {}".format(COLUMNDEFAULT_INCLUDE_QUOTE_VER))
        self.get_table_list()
        pg_conn = self.connect_db()
        # table = self.table_list[0]
        for table in self.table_list:
            # create table
            self.logger.info("table: {}".format(table))
            self.create_table(table)
            # create index
            self.create_index_process(table)
            # break
            # load data

            real_data_path = os.path.join(self.out_dir, self.source_schema)
            allfiles = os.listdir(real_data_path)
            files = [fname for fname in allfiles if re.search('{}_slice'.format(table), fname)]

            for file in files:
                self.logger.info("{} file {}".format(table, file))
                csv_file_name = os.path.join(real_data_path, file)
                self.copy_table_data(table, csv_file_name, pg_conn)
            continue


if __name__ == '__main__':
    user = 'kedacom'
    host = '172.16.80.191'
    port = 9242
    password = 'Keda!Mysql_36'
    pg = pg_engine(host=host, user=user, port=port, password=password)
    pg.run()

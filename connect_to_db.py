import pymysql
import pymysql.cursors

from common_funcs import get_logger
from config import mysql_con_details


log = get_logger(__name__)


class LoggingCursor(pymysql.cursors.Cursor):
    def execute(self, sql, args=None):
        query = self.mogrify(sql, args) if args else sql
        log.debug(f"Executing query:\n{query}")
        return super().execute(sql, args)


def get_db_con(db_name='neoshare_lake')-> pymysql.Connection:
    log.info('Connected to MySQL DB')
    con = pymysql.connect(
        host=mysql_con_details.host,
        port=mysql_con_details.port,
        user=mysql_con_details.user,
        db=db_name
    )
    return con

def get_logging_db_con(db_name='neoshare_lake')-> pymysql.Connection:
    log.info('Connected to MySQL DB')
    con = pymysql.connect(
        host=mysql_con_details.host,
        port=mysql_con_details.port,
        user=mysql_con_details.user,
        db=db_name,
        cursorclass=LoggingCursor
    )
    return con

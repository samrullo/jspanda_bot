import mysql.connector as mcon
from conf.mysql import get_mysql_db_info


class Model:
    def __init__(self):
        self.mysql_conf = get_mysql_db_info()
        self.mydb = mcon.connect(**self.mysql_conf)
        self.table = ""

    def get_item(self, id):
        stmt = "SELECT * FROM {} WHERE id=%s".format(self.table)
        args = (id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        return cursor.fetchone()

    def get_items(self):
        stmt = "SELECT * FROM {}".format(self.table)
        cursor = self.mydb.cursor()
        cursor.execute(stmt)
        return cursor.fetchall()

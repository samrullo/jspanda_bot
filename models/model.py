import mysql.connector as mcon
from conf.mysql import get_mysql_db_info


class Model:
    def __init__(self):
        self.mysql_conf = get_mysql_db_info()
        self.mydb = mcon.connect(host=self.mysql_conf['host'], user=self.mysql_conf['user'], passwd=self.mysql_conf['passwd'], database=self.mysql_conf['database'])

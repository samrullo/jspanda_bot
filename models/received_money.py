from models.model import Model
from conf.mysql import get_mysql_db_info
from utils.utils import to_yyyymmdd


class ReceivedMoney(Model):
    def __init__(self):
        super().__init__()
        self.table = 'received_money'

    def get_items(self):
        stmt = "SELECT * FROM {} ORDER BY registered_date DESC".format(self.table)
        cursor = self.mydb.cursor()
        cursor.execute(stmt)
        return cursor.fetchall()

    def add_item(self, date, amount_usd, exchange_rate):
        amount_jpy = amount_usd * exchange_rate
        statement = f"INSERT INTO `{self.table}`(`registered_date`,`amount_usd`,`exchange_rate`,`amount_jpy`) VALUES(%s,%s,%s,%s)"
        cursor = self.mydb.cursor()
        cursor.execute(statement, [to_yyyymmdd(date), amount_usd, exchange_rate, amount_jpy])
        self.mydb.commit()
        return

    def update_item(self, id, date, amount_usd, exchange_rate):
        amount_jpy = amount_usd * exchange_rate
        statement = f"UPDATE `{self.table}` SET `registered_date`=%s,`amount_usd`=%s,`exchange_rate`=%s,`amount_jpy`=%s WHERE `id`={id}"
        cursor = self.mydb.cursor()
        cursor.execute(statement, [to_yyyymmdd(date), amount_usd, exchange_rate, amount_jpy])
        self.mydb.commit()
        return

    def remove_item(self, id):
        statement = f"DELETE FROM {self.table} WHERE id=(%s)"
        cursor = self.mydb.cursor()
        cursor.execute(statement, [id])
        self.mydb.commit()
        return

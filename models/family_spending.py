from models.model import Model
import pandas as pd
from utils.utils import to_yyyymmdd
import logging


class FamilySpending(Model):
    def __init__(self):
        super().__init__()
        self.table = "family_spending"

    def create_table(self):
        statement = f"CREATE TABLE IF NOT EXISTS `{self.table}`(`id` INT AUTO_INCREMENT, `date` DATE, `name` VARCHAR(200), `amount` INT, PRIMARY KEY (`id`))"
        cursor = self.mydb.cursor()
        cursor.execute(statement)
        self.mydb.commit()
        logging.info(f"created table {self.table}")
        return

    def add_item(self, date, name, amount):
        statement = f"INSERT INTO `{self.table}`(`date`,`name`,`amount`) VALUES(%s,%s,%s)"
        cursor = self.mydb.cursor()
        cursor.execute(statement, [to_yyyymmdd(date), name, amount])
        self.mydb.commit()
        logging.info(f"added family spending with {date},{name},{amount}")
        return

    def update_item(self, id, date, name, amount):
        statement = f"UPDATE `{self.table}` SET `date`=%s,`name`=%s,`amount`=%s WHERE `id`={id}"
        cursor = self.mydb.cursor()
        cursor.execute(statement, [to_yyyymmdd(date), name, amount])
        self.mydb.commit()
        logging.info(f"update family spending {id} with {date},{name},{amount}")
        return

    def get_items_by_date(self, date):
        statement = f"SELECT * FROM {self.table} WHERE `date`=%s"
        cursor = self.mydb.cursor()
        cursor.execute(statement, [date])
        return cursor.fetchall()

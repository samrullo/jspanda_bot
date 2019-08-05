import sqlite3
from models.model import Model
import mysql.connector as mcon
from conf.mysql import get_mysql_db_info
from models.product_category import Product_category


class Product(Model):
    def __init__(self, dbname='jspanda.sqlite', product_category: Product_category = None):
        super().__init__()
        self.dbname = dbname
        self.table = 'product'
        self.conn = sqlite3.connect(dbname)
        self.product_category = product_category
        self.name = ""
        self.photo = ""
        self.description = ""
        self.price = 0
        self.category_id = 0
        self.last_product_id = 0

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS {}(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), price INT, photo VARCHAR(255))".format(self.table)
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, name=None, description=None, price=None, photo=None):
        stmt = "INSERT INTO {}(name, description, price, photo) VALUES (%s,%s,%s,%s)".format(self.table)
        args = (name, description, price, photo)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        product_id = cursor.lastrowid
        self.mydb.commit()
        return product_id

    def delete_item(self, id):
        stmt = "DELETE FROM {} WHERE id=%d".format(self.table)
        args = (id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        self.mydb.commit()

    def get_item(self, id):
        stmt = "SELECT id,name,description,price,photo FROM {} WHERE id=%s".format(self.table)
        args = (id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        return cursor.fetchone()

    def get_items(self):
        stmt = "SELECT id,name,description,price,photo FROM {}".format(self.table)
        cursor = self.mydb.cursor()
        cursor.execute(stmt)
        return cursor.fetchall()

    def set_category(self, product_id, category_id):
        self.product_category.add_item(product_id, category_id)

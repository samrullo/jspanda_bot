import logging
from models.model import Model
from models.productcategory import ProductCategory


class Product(Model):
    def __init__(self, product_category: ProductCategory = None):
        super().__init__()
        self.table = 'product'
        self.product_category = product_category
        self.name = ""
        self.photo = ""
        self.description = ""
        self.price = 0
        self.category_id = 0
        self.last_product_id = 0

    def add_item(self, name=None, description=None, price=None, photo=None):
        stmt = "INSERT INTO {}(name, description, price, photo) VALUES (%s,%s,%s,%s)".format(self.table)
        args = (name, description, price, photo)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        product_id = cursor.lastrowid
        self.mydb.commit()
        return product_id

    def delete_item(self, id):
        logging.info("Start removing product with id {}".format(id))
        self.product_category.delete_by_product_id(id)
        stmt = "DELETE FROM {} WHERE id=%s".format(self.table)
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

    def update_product(self, id, field, new_value):
        logging.info("Will update {} field of product with id {} to {}".format(field, id, new_value))
        stmt = "UPDATE {} SET {}=%s WHERE id=%s".format(self.table, field)
        args = (new_value, id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        product_id = cursor.lastrowid
        self.mydb.commit()
        return product_id

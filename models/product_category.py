from models.model import Model


class Product_category(Model):
    def __init__(self):
        super().__init__()
        self.table = 'product_category'

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS {}(id INT AUTO_INCREMENT PRIMARY KEY, product_id INTEGER, category_id INTEGER)".format(self.table)
        return stmt

    def add_item(self, product_id=None, category_id=None):
        stmt = "INSERT INTO {}(product_id, category_id) VALUES (%s,%s)".format(self.table)
        args = (product_id, category_id)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        self.mydb.commit()

    def delete_item(self, id):
        stmt = "DELETE FROM {} WHERE id=(%s)".format(self.table)
        args = (id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        self.mydb.commit()

    def delete_by_product_id(self, product_id):
        stmt = "DELETE FROM {} WHERE product_id=%s".format(self.table)
        args = (product_id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        self.mydb.commit()

    def get_items(self):
        stmt = "SELECT id,product_id,category_id FROM {}".format(self.table)
        cursor = self.mydb.cursor()
        cursor.execute(stmt)
        return cursor.fetchall()

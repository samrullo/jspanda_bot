from models.model import Model


class Category(Model):
    def __init__(self):
        super().__init__()
        self.table = 'category'
        self.name = ""
        self.description = ""

    def add_item(self, name=None, description=None):
        stmt = "INSERT INTO {}(name, description) VALUES (%s,%s)".format(self.table)
        args = (name, description)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        category_id = cursor.lastrowid
        self.mydb.commit()
        return category_id

    def delete_item(self, id):
        stmt = "DELETE FROM {} WHERE id=%s".format(self.table)
        args = (id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        self.mydb.commit()

    def get_item(self, id):
        stmt = "SELECT id,name,description FROM {} WHERE id=%s".format(self.table)
        args = (id,)
        cursor = self.mydb.cursor()
        cursor.execute(stmt, args)
        return cursor.fetchone()

    def get_items(self):
        stmt = "SELECT id, name, description FROM {}".format(self.table)
        cursor = self.mydb.cursor()
        cursor.execute(stmt)
        return cursor.fetchall()

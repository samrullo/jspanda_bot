from models.product import Product


class ProductController:
    def __init__(self):
        self.product = Product()
        self.is_product_name_set=False
        self.is_product_description_set=False
        self.is_product_photo_set=False
        self.is_product_price_set=False

    def set_product_name(self):
        pass

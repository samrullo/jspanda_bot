import logging
from utils.bot_utils import BotUtil
from models.product import Product
from models.productcategory import ProductCategory
from models.category import Category

butil = BotUtil()


class ProductController:
    def __init__(self, product: Product, category: Category):
        self.product = product
        self.category = category

    def show_products(self, chat_id):
        logging.info("/showproducts command was passed so will send info about all products")
        products = self.product.get_items()
        if len(products) != 0:
            for product_record in products:
                butil.send_product_info(product_record, chat_id)
        else:
            butil.send_message("There are no products in database", chat_id)

    def create_product(self, chat_id, update, text, what_to_do):
        if what_to_do == 'set_product_name':
            logging.info("Was waiting for product name and user should have returned product name : {}".format(text))
            self.product.name = text
            butil.send_message("Enter product description", chat_id)
            return 'set_product_description'
        if what_to_do == 'set_product_description':
            logging.info("Was waiting for product description and user should have returned product description : {}".format(text))
            self.product.description = text
            butil.send_message("Enter product price", chat_id)
            return 'set_product_price'
        if what_to_do == 'set_product_price':
            logging.info("Was waiting for price : {}".format(text))
            if not isinstance(int(text), int):
                butil.send_message("Price should be integer. Enter correct price", chat_id)
                return 'set_product_price'
            self.product.price = text
            butil.send_message("Upload product photo", chat_id)
            return 'set_product_photo'
        if what_to_do == 'set_product_photo':
            logging.info("Was waiting for photo upload, photo id : {}".format(update['message']['photo'][-1]['file_id']))
            self.product.photo = update['message']['photo'][-1]['file_id']
            product_id = self.product.add_item(self.product.name, self.product.description, self.product.price, self.product.photo)
            product_record = self.product.get_item(product_id)
            msg = "Registered new product.\n Product id : {product_id} \n Product name : {name} \n Product description : {description} \n Product price : {price} \n".format(product_id=product_record[0],
                                                                                                                                                                             name=product_record[1],
                                                                                                                                                                             description=product_record[2],
                                                                                                                                                                             price=product_record[3])
            butil.send_photo(msg, chat_id, product_record[4])
            self.product.last_product_id = product_id
            logging.info("finished sending photo and setting last_product_id {}".format(self.product.last_product_id))
            logging.info("Will send prompt to choose categories.")
            reply_markup = butil.build_categories_inline_keyboard(self.category.get_items())
            butil.send_message("Choose category for the product", chat_id, reply_markup)
            return 'set_product_category'
        if what_to_do == 'set_product_category':
            logging.info("User should have sent category id with callback query : {}".format(text))
            self.product.set_category(self.product.last_product_id, text)
            msg = "Set product category.\n Product id : {} \n Category id : {} \n".format(self.product.last_product_id, text)
            butil.send_message(msg, chat_id)
        else:
            logging.info("newproduct command was passed, so will send message to ask for product name")
            butil.send_message("Enter product name", chat_id)
            return 'set_product_name'

    def product_edit_choose(self, chat_id, text):
        logging.info("User chose to edit product {}".format(text))
        if len(text.split('|')) == 2:
            logging.info("Edit product initiated. Will send message with choices to ask user what to edit.")
            product_id = int(text.split('|')[1])
            product_record = self.product.get_item(product_id)
            reply_markup = butil.build_edit_product_choices_inline_keyboard(product_record)
            butil.send_message("Choose what you want to edit", chat_id, reply_markup)
        elif len(text.split('|')) == 3:
            product_id = int(text.split('|')[-1])
            action = text.split('|')[1]
            if action in ('name', 'description', 'price'):
                butil.send_message('Enter new {}'.format(action), chat_id)
                return 'update_product|{}|{}'.format(action, product_id)
            else:
                butil.send_message("Upload new photo", chat_id)
                return 'update_product|{}|{}'.format(action, product_id)

    def product_edit(self, what_to_do, chat_id, text, update):
        product_id = int(what_to_do.split('|')[-1])
        field = what_to_do.split('|')[1]
        if field in ('name', 'description', 'price'):
            new_value = text
            self.product.update_product(product_id, field, new_value)
            updated_product_record = self.product.get_item(product_id)
            butil.send_product_info(updated_product_record, chat_id)
        elif field == 'photo':
            new_value = update['message']['photo'][-1]['file_id']
            self.product.update_product(product_id, field, new_value)
            updated_product_record = self.product.get_item(product_id)
            butil.send_product_info(updated_product_record, chat_id)

    def remove_product(self, text):
        logging.info("User chose to remove product {}".format(text))
        product_id = int(text.split('|')[1])
        product_record = self.product.get_item(product_id)
        self.product.delete_item(product_id)
        msg = " Removed following product. \n Product id : {product_id} \n Product name : {name} \n Product description : {description}\n Product price : {price} ".format(product_id=product_record[0],
                                                                                                                                                                           name=product_record[1],
                                                                                                                                                                           description=product_record[2],
                                                                                                                                                                           price=product_record[3]
                                                                                                                                                                           )
        return msg

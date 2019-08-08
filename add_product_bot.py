import json
import requests
import urllib
import time
from models.product import Product
from models.category import Category
from models.productcategory import ProductCategory
from conf.tokens import get_token
import logging
from utils.bot_utils import BotUtil
from controllers.category_controller import CategoryController

product_category = ProductCategory()
product = Product(product_category=product_category)
category = Category()

butil = BotUtil()
categ_cont = CategoryController()


def handle_update(update, what_to_do):
    try:
        logging.info("Update result:{}".format(update))
        if 'callback_query' in update.keys():
            text = update['callback_query']['data']
            chat_id = update['callback_query']['message']['chat']['id']
        else:
            if 'text' in update['message'].keys():
                text = update['message']['text']
            else:
                text = ""
            chat_id = update['message']['chat']['id']

        # if help command is passed send set options from which to choose
        if text == '/help':
            butil.show_help_message(chat_id)

        # handling new categories
        if text == '/newcategory':
            logging.info("newcategory command was passed, so will start process to set up new category. First will send message to ask for category name")
            butil.send_message('Enter category name', chat_id)
            return 'set_category_name'
        if what_to_do == 'set_category_name':
            logging.info("Was expecting category name, so will set category name")
            category.name = text
            butil.send_message("Enter category description", chat_id)
            return 'set_category_description'
        if what_to_do == 'set_category_description':
            logging.info("Was expecting category description, so will set category description")
            category.description = text
            category_id = category.add_item(category.name, category.description)
            category_record = category.get_item(category_id)
            msg = "Recorded new category. \n Category id : {category_id} \n Category name : {name} \n Category Description : {description}\n".format(category_id=category_record[0],
                                                                                                                                                     name=category_record[1],
                                                                                                                                                     description=category_record[2]
                                                                                                                                                     )
            butil.send_message(msg, chat_id)

        # handling new product registration
        if text == '/newproduct':
            logging.info("newproduct command was passed, so will send message to ask for product name")
            butil.send_message("Enter product name", chat_id)
            return 'set_product_name'
        if what_to_do == 'set_product_name':
            logging.info("Was waiting for product name and user should have returned product name : {}".format(text))
            product.name = text
            butil.send_message("Enter product description", chat_id)
            return 'set_product_description'
        if what_to_do == 'set_product_description':
            logging.info("Was waiting for product description and user should have returned product description : {}".format(text))
            product.description = text
            butil.send_message("Enter product price", chat_id)
            return 'set_product_price'
        if what_to_do == 'set_product_price':
            logging.info("Was waiting for price : {}".format(text))
            if not isinstance(int(text), int):
                butil.send_message("Price should be integer. Enter correct price", chat_id)
                return 'set_product_price'
            product.price = text
            butil.send_message("Upload product photo", chat_id)
            return 'set_product_photo'
        if what_to_do == 'set_product_photo':
            logging.info("Was waiting for photo upload, photo id : {}".format(update['message']['photo'][-1]['file_id']))
            product.photo = update['message']['photo'][-1]['file_id']
            product_id = product.add_item(product.name, product.description, product.price, product.photo)
            product_record = product.get_item(product_id)
            msg = "Registered new product.\n Product id : {product_id} \n Product name : {name} \n Product description : {description} \n Product price : {price} \n".format(product_id=product_record[0],
                                                                                                                                                                             name=product_record[1],
                                                                                                                                                                             description=product_record[2],
                                                                                                                                                                             price=product_record[3])
            butil.send_photo(msg, chat_id, product_record[4])
            product.last_product_id = product_id
            logging.info("finished sending photo and setting last_product_id {}".format(product.last_product_id))
            logging.info("Will send prompt to choose categories.")
            reply_markup = butil.build_categories_inline_keyboard(category.get_items())
            butil.send_message("Choose category for the product", chat_id, reply_markup)
            return 'set_product_category'
        if what_to_do == 'set_product_category':
            logging.info("User should have sent category id with callback query : {}".format(text))
            product.set_category(product.last_product_id, text)
            msg = "Set product category.\n Product id : {} \n Category id : {} \n".format(product.last_product_id, text)
            butil.send_message(msg, chat_id)

        # show all products
        if text == '/showproducts':
            logging.info("showproducts command was passed so will send info about all products")
            products = product.get_items()
            if len(products) != 0:
                for product_record in products:
                    butil.send_product_info(product_record, chat_id)
            else:
                butil.send_message("There are no products in database", chat_id)

        # handle remove product
        if 'remove_product' in text:
            logging.info("User chose to remove product {}".format(text))
            product_id = int(text.split('|')[1])
            product_record = product.get_item(product_id)
            product.delete_item(product_id)
            msg = "Removed following product. \n Product id : {product_id} \n Product name : {name} \n Product description : {description} \n Product price : {price} \n".format(product_id=product_record[0],
                                                                                                                                                                                 name=product_record[1],
                                                                                                                                                                                 description=product_record[2],
                                                                                                                                                                                 price=product_record[3])
            butil.send_message(msg, chat_id)

        # handle edit product
        if 'edit_product' in text:
            logging.info("User chose to edit product {}".format(text))
            if len(text.split('|')) == 2:
                logging.info("Edit product initiated. Will send message with choices to ask user what to edit.")
                product_id = int(text.split('|')[1])
                product_record = product.get_item(product_id)
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
        if what_to_do:
            if 'update_product' in what_to_do:
                product_id = int(what_to_do.split('|')[-1])
                field = what_to_do.split('|')[1]
                if field in ('name', 'description', 'price'):
                    new_value = text
                    product.update_product(product_id, field, new_value)
                    updated_product_record = product.get_item(product_id)
                    butil.send_product_info(updated_product_record, chat_id)
                elif field == 'photo':
                    new_value = update['message']['photo'][-1]['file_id']
                    product.update_product(product_id, field, new_value)
                    updated_product_record = product.get_item(product_id)
                    butil.send_product_info(updated_product_record, chat_id)

        # handle showcategory command
        if text == '/showcategories':
            categ_cont.show_categories(chat_id)

        # handle remove category
        if 'remove_category' in text:
            msg = categ_cont.remove_category(text)
            butil.send_message(msg, chat_id)

        # handle edit category
        if 'edit_category' in text:
            return categ_cont.category_edit_choose(chat_id, text)

        if what_to_do:
            if 'update_category' in what_to_do:
                categ_cont.category_edit(what_to_do, chat_id, text)

    except KeyError as e:
        print(e)

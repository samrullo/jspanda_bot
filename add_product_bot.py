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
from controllers.product_controller import ProductController

product_category = ProductCategory()
product = Product(product_category=product_category)
category = Category(product_category)

butil = BotUtil()
categ_cont = CategoryController(category)
product_cont = ProductController(product, category)


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
        if text == '/newcategory' or what_to_do in ('set_category_name','set_category_description'):
            return categ_cont.create_category(chat_id, text, what_to_do)

        # handling new product registration
        if text == '/newproduct' or what_to_do in ('set_product_name', 'set_product_description', 'set_product_price', 'set_product_photo'):
            return product_cont.create_product(chat_id, update, text, what_to_do)

        # show all products
        if text == '/showproducts':
            product_cont.show_products(chat_id)

        # handle remove product
        if 'remove_product' in text:
            msg = product_cont.remove_product(text)
            butil.send_message(msg, chat_id)

        # handle edit product
        if 'edit_product' in text:
            product_cont.product_edit_choose(chat_id, text)

        if what_to_do:
            if 'update_product' in what_to_do:
                product_cont.product_edit(what_to_do, chat_id, text, update)

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

import json
import requests
import urllib
import time
from models.product import Product
from models.category import Category
from models.product_category import Product_category
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
_logger = logging.getLogger(__file__)

TOKEN = "365379007:AAFN0M2gifkBuVlLPQbSdl_DqrSsazqY8Qc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
product_category = Product_category()
product = Product(product_category=product_category)
category = Category()


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + 'getUpdates?timeout=100'
    if offset:
        url += '&offset={}'.format(offset)
    updates = get_json_from_url(url)
    return updates


def get_last_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(update['update_id'])
    return max(update_ids)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}
    return json.dumps(reply_markup)


def build_inline_keyboard(items):
    keyboard = [[{'text': item['label'], 'callback_data': item['command']}] for item in items]
    reply_markup = {'inline_keyboard': keyboard}
    return json.dumps(reply_markup)


def build_categories_inline_keyboard(categories):
    keyboard = [[{'text': category[1], 'callback_data': category[0]}] for category in categories]
    reply_markup = {'inline_keyboard': keyboard}
    return json.dumps(reply_markup)


def build_product_inline_keyboard(product_record):
    keyboard = [
        [{'text': "Edit product", 'callback_data': "edit_product|{}".format(product_record[0])}],
        [{'text': "Remove product", 'callback_data': "remove_product|{}".format(product_record[0])}]
    ]
    reply_markup = {'inline_keyboard': keyboard}
    return json.dumps(reply_markup)


def build_edit_product_choices_inline_keyboard(product_record):
    keyboard = \
        [
            [{'text': 'Edit product name', 'callback_data': 'edit_product|name|{}'.format(product_record[0])}],
            [{'text': 'Edit product description', 'callback_data': 'edit_product|description|{}'.format(product_record[0])}],
            [{'text': 'Edit product price', 'callback_data': 'edit_product|price|{}'.format(product_record[0])}],
            [{'text': 'Edit product photo', 'callback_data': 'edit_product|photo|{}'.format(product_record[0])}]
        ]
    reply_markup = {'inline_keyboard': keyboard}
    return json.dumps(reply_markup)


def send_product_info(product_record, chat_id):
    msg = "Product id : {product_id} \n Product name : {name} \n Product description : {description} \n Product price : {price} \n".format(product_id=product_record[0],
                                                                                                                                           name=product_record[1],
                                                                                                                                           description=product_record[2],
                                                                                                                                           price=product_record[3])
    reply_markup = build_product_inline_keyboard(product_record)
    send_photo(msg, chat_id, product_record[4])
    send_message("Choose action", chat_id, reply_markup)


def get_last_chat_id_and_text(updates):
    result_records = updates['result']
    last_id = len(result_records) - 1
    text = result_records[last_id]['message']['text']
    chat_id = result_records[last_id]['message']['chat']['id']
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(chat_id, text)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    logging.info("sendMessage url : {}".format(url))
    get_url(url)


def send_photo(text, chat_id, photo_file_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendPhoto?chat_id={}&photo={}&caption={}&parse_mode=Markdown".format(chat_id, photo_file_id, text)
    logging.info("Will get url : {}".format(url))
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    logging.info("sendPhoto url : {}".format(url))
    get_url(url)


def handle_updates(updates, what_to_do):
    for update in updates['result']:
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
                reply_markup = build_inline_keyboard([{'label': 'Register new product', 'command': '/newproduct'},
                                                      {'label': 'Register new category', 'command': '/newcategory'},
                                                      {'label': 'Show all products', 'command': '/showproducts'}, ])
                send_message("Choose what you want to do", updates['result'][0]['message']['chat']['id'], reply_markup)

            # handling new categories
            if text == '/newcategory':
                logging.info("newcategory command was passed, so will start process to set up new category. First will send message to ask for category name")
                send_message('Enter category name', chat_id)
                return 'set_category_name'
            if what_to_do == 'set_category_name':
                logging.info("Was expecting category name, so will set category name")
                category.name = text
                send_message("Enter category description", chat_id)
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
                send_message(msg, chat_id)

            # handling new product registration
            if text == '/newproduct':
                logging.info("newproduct command was passed, so will send message to ask for product name")
                send_message("Enter product name", chat_id)
                return 'set_product_name'
            if what_to_do == 'set_product_name':
                logging.info("Was waiting for product name and user should have returned product name : {}".format(text))
                product.name = text
                send_message("Enter product description", chat_id)
                return 'set_product_description'
            if what_to_do == 'set_product_description':
                logging.info("Was waiting for product description and user should have returned product description : {}".format(text))
                product.description = text
                send_message("Enter product price", chat_id)
                return 'set_product_price'
            if what_to_do == 'set_product_price':
                logging.info("Was waiting for price : {}".format(text))
                if not isinstance(int(text), int):
                    send_message("Price should be integer. Enter correct price", chat_id)
                    return 'set_product_price'
                product.price = text
                send_message("Upload product photo", chat_id)
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
                send_photo(msg, chat_id, product_record[4])
                product.last_product_id = product_id
                logging.info("finished sending photo and setting last_product_id {}".format(product.last_product_id))
                logging.info("Will send prompt to choose categories.")
                reply_markup = build_categories_inline_keyboard(category.get_items())
                send_message("Choose category for the product", chat_id, reply_markup)
                return 'set_product_category'
            if what_to_do == 'set_product_category':
                logging.info("User should have sent category id with callback query : {}".format(text))
                product.set_category(product.last_product_id, text)
                msg = "Set product category.\n Product id : {} \n Category id : {} \n".format(product.last_product_id, text)
                send_message(msg, chat_id)

            # show all products
            if text == '/showproducts':
                logging.info("showproducts command was passed so will send info about all products")
                products = product.get_items()
                if len(products) != 0:
                    for product_record in products:
                        send_product_info(product_record, chat_id)
                else:
                    send_message("There are no products in database", chat_id)

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
                send_message(msg, chat_id)

            # handle edit product
            if 'edit_product' in text:
                logging.info("User chose to edit product {}".format(text))
                if len(text.split('|')) == 2:
                    logging.info("Edit product initiated. Will send message with choices to ask user what to edit.")
                    product_id = int(text.split('|')[1])
                    product_record = product.get_item(product_id)
                    reply_markup = build_edit_product_choices_inline_keyboard(product_record)
                    send_message("Choose what you want to edit", chat_id, reply_markup)
                elif len(text.split('|')) == 3:
                    product_id = int(text.split('|')[-1])
                    action = text.split('|')[1]
                    if action in ('name', 'description', 'price'):
                        send_message('Enter new {}'.format(action), chat_id)
                        return 'update_product|{}|{}'.format(action, product_id)
                    else:
                        send_message("Upload new photo", chat_id)
                        return 'update_product|{}|{}'.format(action, product_id)
            if what_to_do:
                if 'update_product' in what_to_do:
                    product_id = int(what_to_do.split('|')[-1])
                    field = what_to_do.split('|')[1]
                    if field in ('name', 'description', 'price'):
                        new_value = text
                        product.update_product(product_id, field, new_value)
                        updated_product_record = product.get_item(product_id)
                        send_product_info(updated_product_record, chat_id)
                    elif field == 'photo':
                        new_value = update['message']['photo'][-1]['file_id']
                        product.update_product(product_id, field, new_value)
                        updated_product_record = product.get_item(product_id)
                        send_product_info(updated_product_record, chat_id)
        except KeyError as e:
            print(e)


def main():
    logging.info("Finished setting up database tables product and category")
    last_update_id = None
    what_to_do = ""
    logging.info("Will start eternal loop")
    while True:
        updates = get_updates(last_update_id)
        logging.info("Updates : {}".format(updates))
        if len(updates['result']) > 0:
            last_update_id = get_last_update_id(updates) + 1
            what_to_do = handle_updates(updates, what_to_do)
        time.sleep(0.5)


if __name__ == '__main__':
    _logger.info("Start the show...")
    main()

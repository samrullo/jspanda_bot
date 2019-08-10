import json
import requests
import urllib
import logging
from conf.tokens import get_token
from conf.tokens import get_telegraph_token


class BotUtil:
    def __init__(self):
        TOKEN = get_token()
        URL = "https://api.telegram.org/bot{}/".format(TOKEN)
        self.URL = URL
        self.telegraph_url = """https://api.telegra.ph/createPage?access_token={}""".format(get_telegraph_token())

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.URL + 'getUpdates?timeout=100'
        if offset:
            url += '&offset={}'.format(offset)
        updates = self.get_json_from_url(url)
        return updates

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates['result']:
            update_ids.append(update['update_id'])
        return max(update_ids)

    def build_keyboard(self, items):
        keyboard = [[item] for item in items]
        reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}
        return json.dumps(reply_markup)

    def build_inline_keyboard(self, items):
        keyboard = [[{'text': item['label'], 'callback_data': item['command']}] for item in items]
        reply_markup = {'inline_keyboard': keyboard}
        return json.dumps(reply_markup)

    def build_categories_inline_keyboard(self, categories):
        keyboard = [[{'text': category[1], 'callback_data': category[0]}] for category in categories]
        reply_markup = {'inline_keyboard': keyboard}
        return json.dumps(reply_markup)

    def build_product_inline_keyboard(self, product_record):
        keyboard = [
            [{'text': "Edit product", 'callback_data': "edit_product|{}".format(product_record[0])}],
            [{'text': "Remove product", 'callback_data': "remove_product|{}".format(product_record[0])}]
        ]
        reply_markup = {'inline_keyboard': keyboard}
        return json.dumps(reply_markup)

    def build_edit_product_choices_inline_keyboard(self, product_record):
        keyboard = \
            [
                [{'text': 'Edit product name', 'callback_data': 'edit_product|name|{}'.format(product_record[0])}],
                [{'text': 'Edit product description', 'callback_data': 'edit_product|description|{}'.format(product_record[0])}],
                [{'text': 'Edit product price', 'callback_data': 'edit_product|price|{}'.format(product_record[0])}],
                [{'text': 'Edit product photo', 'callback_data': 'edit_product|photo|{}'.format(product_record[0])}]
            ]
        reply_markup = {'inline_keyboard': keyboard}
        return json.dumps(reply_markup)

    def build_category_inline_keyboard(self, category_record):
        keyboard = [
            [{'text': "Edit category", 'callback_data': "edit_category|{}".format(category_record[0])}],
            [{'text': "Remove category", 'callback_data': "remove_category|{}".format(category_record[0])}]
        ]
        reply_markup = {'inline_keyboard': keyboard}
        return json.dumps(reply_markup)

    def build_edit_category_choices_inline_keyboard(self, category_record):
        keyboard = [
            [{'text': 'Edit category name', 'callback_data': 'edit_category|name|{}'.format(category_record[0])}],
            [{'text': 'Edit category description', 'callback_data': 'edit_category|description|{}'.format(category_record[0])}]
        ]
        reply_markup = {'inline_keyboard': keyboard}
        return json.dumps(reply_markup)

    def send_product_info(self, product_record, chat_id):
        msg = "Product id : {product_id} \n Product name : {name} \n Product description : {description} \n Product price : {price} \n".format(product_id=product_record[0],
                                                                                                                                               name=product_record[1],
                                                                                                                                               description=product_record[2],
                                                                                                                                               price=product_record[3])
        reply_markup = self.build_product_inline_keyboard(product_record)
        self.send_photo(msg, chat_id, product_record[4])
        self.send_message("Choose action", chat_id, reply_markup)

    def send_category_info(self, category_record, chat_id):
        msg = " Category id : {category_id}\n Category name : {name}\n Category description : {description}".format(category_id=category_record[0],
                                                                                                                    name=category_record[1],
                                                                                                                    description=category_record[2])
        reply_markup = self.build_category_inline_keyboard(category_record)
        self.send_message(msg + "\n Choose action", chat_id, reply_markup)

    def get_last_chat_id_and_text(self, updates):
        result_records = updates['result']
        last_id = len(result_records) - 1
        text = result_records[last_id]['message']['text']
        chat_id = result_records[last_id]['message']['chat']['id']
        return (text, chat_id)

    def send_message(self, text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = self.URL + "sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(chat_id, text)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        logging.info("sendMessage url : {}".format(url))
        self.get_url(url)

    def send_photo(self, text, chat_id, photo_file_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = self.URL + "sendPhoto?chat_id={}&photo={}&caption={}&parse_mode=Markdown".format(chat_id, photo_file_id, text)
        logging.info("Will get url : {}".format(url))
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        logging.info("sendPhoto url : {}".format(url))
        self.get_url(url)

    def show_help_message(self, chat_id):
        reply_markup = self.build_inline_keyboard([{'label': 'Register new product', 'command': '/newproduct'},
                                                   {'label': 'Register new category', 'command': '/newcategory'},
                                                   {'label': 'Show all products', 'command': '/showproducts'},
                                                   {'label': 'Show all categories', 'command': '/showcategories'}
                                                   ])
        self.send_message("Choose what you want to do", chat_id, reply_markup)

import logging
from utils.bot_utils import BotUtil
from models.category import Category
from models.product import Product
from models.productcategory import ProductCategory

butil = BotUtil()


class CategoryController:
    def __init__(self, category: Category):
        self.category = category

    def create_category(self, chat_id, text, what_to_do):
        if what_to_do == 'set_category_name':
            logging.info("Was expecting category name, so will set category name")
            self.category.name = text
            butil.send_message("Enter category description", chat_id)
            return 'set_category_description'
        if what_to_do == 'set_category_description':
            logging.info("Was expecting category description, so will set category description")
            self.category.description = text
            category_id = self.category.add_item(self.category.name, self.category.description)
            category_record = self.category.get_item(category_id)
            msg = "Recorded new category. \n Category id : {category_id} \n Category name : {name} \n Category Description : {description}\n".format(category_id=category_record[0],
                                                                                                                                                     name=category_record[1],
                                                                                                                                                     description=category_record[2]
                                                                                                                                                     )
            butil.send_message(msg, chat_id)
        else:
            logging.info("newcategory command was passed, so will start process to set up new category. First will send message to ask for category name")
            butil.send_message('Enter category name', chat_id)
            return 'set_category_name'

    def category_edit_choose(self, chat_id, text):
        logging.info("User chose to edit category {}".format(text))
        if len(text.split('|')) == 2:
            logging.info("Edit category initiated. Will send message with choices to ask user what to edit.")
            category_id = int(text.split('|')[1])
            category_record = self.category.get_item(category_id)
            reply_markup = butil.build_edit_category_choices_inline_keyboard(category_record)
            butil.send_message("Choose what you want to edit", chat_id, reply_markup)
        elif len(text.split('|')) == 3:
            category_id = int(text.split('|')[-1])
            action = text.split('|')[1]
            if action in ('name', 'description'):
                butil.send_message('Enter new {}'.format(action), chat_id)
                return 'update_category|{}|{}'.format(action, category_id)
            else:
                butil.send_message("Upload new photo", chat_id)
                return 'update_category|{}|{}'.format(action, category_id)

    def category_edit(self, what_to_do, chat_id, text):
        category_id = int(what_to_do.split('|')[-1])
        field = what_to_do.split('|')[1]
        if field in ('name', 'description'):
            new_value = text
            self.category.update_category(category_id, field, new_value)
            updated_category_record = self.category.get_item(category_id)
            butil.send_category_info(updated_category_record, chat_id)

    def show_categories(self, chat_id):
        logging.info("showcategory command was passed so will send info about all categories")
        categories = self.category.get_items()
        if len(categories) != 0:
            for category_record in categories:
                butil.send_category_info(category_record, chat_id)
        else:
            butil.send_message("There are no categories in database", chat_id)

    def remove_category(self, text):
        logging.info("User chose to remove category {}".format(text))
        category_id = int(text.split('|')[1])
        category_record = self.category.get_item(category_id)
        self.category.delete_item(category_id)
        msg = " Removed following category. \n Category id : {category_id} \n Category name : {name} \n Category description : {description} ".format(category_id=category_record[0],
                                                                                                                                                      name=category_record[1],
                                                                                                                                                      description=category_record[2]
                                                                                                                                                      )
        return msg

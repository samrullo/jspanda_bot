from flask import Flask
from flask import request
import os
from flask import session
import json
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
_logger = logging.getLogger(__file__)

from add_product_bot import handle_update

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    update = request.data.decode('utf8')
    update = json.loads(update)

    with  open(os.path.relpath('session_file'), 'r') as fh:
        what_to_do = fh.readline()
        logging.info("what_to_do before : {}".format(what_to_do))
        what_to_do = handle_update(update, what_to_do)
        logging.info("what_to_do after: {}".format(what_to_do))
    with open(os.path.relpath('session_file'), 'w') as fh:
        fh.write(what_to_do)
    return ""  # it is important as this return 200 success response to telegram


@app.route('/show_session')
def show_session():
    return "what_to_do session : {}".format(session.get('what_to_do'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

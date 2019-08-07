from flask import Flask
from flask import request
from conf.appconf import Config
from flask import session
import json
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
_logger = logging.getLogger(__file__)

from add_product_bot import handle_update

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['POST', 'GET'])
def hello():
    update = request.data.decode('utf8')
    update = json.loads(update)
    logging.info("what_to_do before : {}".format(session.get('what_to_do')))
    what_to_do = session.get('what_to_do')
    session['what_to_do'] = handle_update(update, session.get('what_to_do'))
    while session.get('what_to_do') and session.get('what_to_do') != what_to_do:
        logging.info("what_to_do before : {}".format(session.get('what_to_do')))
        what_to_do = session.get('what_to_do')
        session['what_to_do'] = handle_update(update, session.get('what_to_do'))
        logging.info("what_to_do after: {}".format(session.get('what_to_do')))
    logging.info("what_to_do after: {}".format(session.get('what_to_do')))
    return ""  # it is important as this return 200 success response to telegram


if __name__ == '__main__':
    app.run(host='0.0.0.0')

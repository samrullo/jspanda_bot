from flask import Flask
from flask import request
import json
from add_product_bot import handle_update

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    update = request.data.decode('utf8')
    update = json.loads(update)
    handle_update(update)
    return ""  # it is important as this return 200 success response to telegram


if __name__ == '__main__':
    app.run(host='0.0.0.0')

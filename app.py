import os

from flask import Flask

app = Flask(__name__)

FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT', '8080')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World from Order!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=FLASK_RUN_PORT, debug=True)

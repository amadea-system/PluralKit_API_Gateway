"""
This is an API Gateway for the Plural Kit API.
It's primary purpose is to take the load from our internal programs and scripts
    and thus remove that burden from the Plural Kit servers,


Copyright 2020 Amadea System
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

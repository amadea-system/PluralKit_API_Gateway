"""
This is an API Gateway for the Plural Kit API.
It's primary purpose is to take the load from our internal programs and scripts
    and thus remove that burden from the Plural Kit servers,


Copyright 2020 Amadea System
"""
import logging
import json

from flask import Flask

from utils import pluralKitAPI as pk

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

log = logging.getLogger(__name__)
app = Flask(__name__)

with open('config.json') as conf_file:
    config = json.load(conf_file)
    system_id = config['system_id']
    pk_token = config['pk_token']
    # system_id_debug = config['system_id_debug']
    # pk_token_debug = config['pk_token_debug']

amadea_system = pk.System.get_by_hid(system_id, pk_token)
amadea_system._fronter_decay_time = config['fronter_decay_time']


@app.route('/')
def hello_world():
    return 'Welcome to the PK API Gateway'


@app.route('/raw/s/amadea/fronters')
def get_raw_fronters():
    try:
        amadea_system.update_fronters(forced=True)
        fronters = amadea_system.fronters
    except pk.PluralKitError as e:
        return e
    if fronters.json is not None:
        return fronters.json
    else:
        return {}


@app.route('/s/amadea/fronters')
def get_cached_fronters():
    try:
        fronters = amadea_system.fronters
    except pk.PluralKitError as e:
        return e
    return fronters.json


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    app.run(host="0.0.0.0", debug=False)
    # app.run(host="0.0.0.0", port=8080, debug=True)


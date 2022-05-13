from flask import Flask, jsonify, make_response
from mod.store_v1.controller import store_bp as store_bp_v1
from mod.store_v2.controller import store_bp as store_bp_v2
from mod.store_v3.controller import store_bp as store_bp_v3
from mod.store_v4.controller import store_bp as store_bp_v4
from mod.store_v5.controller import store_bp as store_bp_v5
from common.JSONEncoder import TdarCustomJSONEncoder
from flask_cors import cross_origin

app = Flask(__name__)
app.json_encoder = TdarCustomJSONEncoder

app.register_blueprint(store_bp_v1, url_prefix='/api/store')
app.register_blueprint(store_bp_v2, url_prefix='/api/v2/store')
app.register_blueprint(store_bp_v3, url_prefix='/api/v3/store')
app.register_blueprint(store_bp_v4, url_prefix='/api/v4/store')
app.register_blueprint(store_bp_v5, url_prefix='/api/v5/store')


@app.errorhandler(Exception)
@cross_origin(origins='*', supports_credentials=True)
def exception_handler(error):
    return make_response(jsonify({'msg': repr(error), 'code': 200}), 200)


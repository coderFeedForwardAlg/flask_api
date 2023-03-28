from flask import Flask

from flask_restful import Api, Resource, request
import numpy as np
import pandas as pd


app = Flask(__name__)
api = Api(app)

class testApi(Resource):
     def get(self, name):
         return {"v3, name is: ": name}

class testApi2(Resource):
     def post(self, food):
         return {"v3, favoret food is: ": food}

@app.route('/json_example', methods=['POST'])
def handle_json():
    data = request.json
    return data

api.add_resource(testApi, "/test/<string:name>")
api.add_resource(testApi2, "/test2/<string:data>")

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
    # app.run()
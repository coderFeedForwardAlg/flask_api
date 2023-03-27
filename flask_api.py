from flask import Flask

from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class testApi(Resource):
     def get(self, name):
         return {"v2, name is: ": name}

api.add_resource(testApi, "/test/<string:name>")

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
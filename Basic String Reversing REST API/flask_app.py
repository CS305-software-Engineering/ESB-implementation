from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class String(Resource):
    def get(self, string):
        rev_string = (str(string))[::-1]
        return {"reversed_string": '{}'.format(rev_string)}


class String2(Resource):
    def get(self):
        return {"message": "Hello!"}


api.add_resource(String2, '/')
api.add_resource(String, '/<string:string>')

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify
from flask_restx import Resource, Api


# instantiate the app
app = Flask(__name__)

api = Api(app)

app.config.from_object('project.config.DevelopmentConfig')


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pawng!'
        }


api.add_resource(Ping, '/ping')
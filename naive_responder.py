from flask import Flask
from flask import render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@app.route('/')
def hello_world():
    return render_template('index.html')

api.add_resource(HelloWorld, '/h')

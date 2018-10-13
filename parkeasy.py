from flask import Flask , jsonify , request , make_response
#from flask_restful import Resource, Api
#from flask_mysqldb import MySQL
#from functools import wraps

import jwt
import datetime

app = Flask(__name__)
api = Api(app)

#home page clause
class Home(Resource):
    def get(self):
        return {"message" : "welcome: This is a homepage"}

#class Users(Resource):

api.add_resource(Home,'/')
#api.add_resource(Users,'/getuser')

if __name__ == '__main__':
    app.run(debug=True)

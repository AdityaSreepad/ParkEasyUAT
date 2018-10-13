from flask import Flask , jsonify , request , make_response
from flask_restful import Resource, Api
#from flask_mysqldb import MySQL
#from functools import wraps

import jwt
import datetime

app = Flask(__name__)

#home page clause
@app.route('/')
def index():
    return 'welcome to the app'
if __name__ == '__main__':
    app.run(debug=True)

'''
from flask import Flask
app = Flask(__name__)

#home page clause
@app.route('/')
def index():
    return 'welcome to the app'

if __name__ == '__main__':
	app.run(debug=True)
'''
from flask import Flask , jsonify , request , make_response
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from functools import wraps

import jwt
import datetime

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root' #'test_user' #'apps'
app.config['MYSQL_PASSWORD'] ='welcome123' #'test'
app.config['MYSQL_DB'] = 'test_db'

app.config['SECRET_KEY'] = '293hdsfhjdfvvrt*739&872dfhude6zvxbnis7&*w(encer!!ksd' #some random value

mysql = MySQL(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({"message" : "token is missing"}),403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"message" : "Invalid token"}),403

        return f(*args, **kwargs)
    return decorated

#_decorator = staticmethod( _decorator )
#from users import get_user_id  >> just an example of how to import methods/functions

#to get user_id based on username
def get_user_id(username):
    cur = mysql.connection.cursor()
    #cur.execute('''SELECT user_id FROM USERS WHERE USER_NAME = %s''',(username))
    sql = ("select user_id from  Users where user_name = '"+username+"'")
    cur.execute(sql)
    user_data = cur.fetchone()
    user_id = int(user_data[0])
    return user_id

#to get location_id based user_id
def get_location(user_id):
    cur = mysql.connection.cursor()
    sql = ("select location_id from locations where plot_owner_id = '"+user_id+"'")
    cur.execute(sql)
    location_id = cur.fetchone()
    location_id = int(location_id[0])
    return location_id

def create_owner_locations(user_id):
    location_data = request.get_json()

    lattitude = location_data['lattitude']
    longitude = location_data['longitude']
    address_line1 = location_data['address_line1']
    address_line2 = location_data['address_line2']
    address_line3 = location_data['address_line3']
    city = location_data['city']
    state= location_data['state']
    zip = location_data['zip']
    loc_attrib1 = location_data['loc_attrib1']
    loc_attrib2 = location_data['loc_attrib2']
    loc_attrib3 = location_data['loc_attrib3']
    loc_attrib4 = location_data['loc_attrib4']
    loc_attrib5 = location_data['loc_attrib5']

    #insert location data into locations table
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO user_locations(plot_owner_id,lattitude,longitude,address_line1,address_line2,address_line3,city,state,zip)
    values (%s , %s , %s , %s , %s , %s, %s, %s, %s)''',(user_id,lattitude,longitude,address_line1,address_line2,address_line3,city,state,zip))
    mysql.connection.commit()

    sql = ("select max(location_id) from user_locations where plot_owner_id = '"+user_id+"'")
    cur.execute(sql)
    location_id = cur.fetchone()
    location_id = int(location_id[0])
    return location_id


def create_owner_site(user_id,location_id):
    user_id = int(user_id)
    location_id = int(location_id)
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO Owner_location_sites(plot_owner_id,plot_location_id) values (%s , %s)''',(user_id,location_id))
    mysql.connection.commit()
    sql = ("select location_site_id from Owner_location_sites where plot_owner_id = '"+user_id+"'"+" AND plot_location_id= '"+location_id)
    cur.execute(sql)
    location_site_id = cur.fetchone()
    location_site_id = int(location_site_id[0])

    return location_site_id


#home page clause
class Home(Resource):
    def get(self):
        return {"message" : "welcome: This is a homepage"}

class Signup(Resource):
    def post(self):
        register_data = request.get_json()
        #return jsonify(login_data) , 201
        uname  = str(register_data['user_name'])
        passwd = str(register_data['password'])

        #connect to Mongo DB
        app.config['MONGO_DBNAME'] ='park_easy_flask_pymongo_db'
        app.config['MONGO_URI'] = 'mongodb://superuser:welcome123@ds255930.mlab.com:55930/park_easy_flask_pymongo_db'

        mongo = pyMongo(app)

        user = mongo.db.users
        user.insert({"name": uname ,"password" : passwd })

        return jsonify({"status" : "Success", "message" : "User registration sucessful, Welcome to ParkEasy "+uname })

class Register(Resource):
    def post(self):
        reg_data = request.get_json()
        #return jsonify(login_data) , 201
        uname  = str(reg_data['user_name'])
        passwd = str(reg_data['password'])

        #cur = mysql.connection.cursor()
        #cur.execute('''select count(*) from  firsttable where table_id >= 100''')
        #rv = cur.fetchone()

        cur = mysql.connection.cursor()
        sql = ("select count(*) from  Users where user_name = '"+uname+"'")  #"'Aditya'"
        #sql = ("select count(*) from  Users where user_name = 'Aditya'")

        cur.execute(sql)
        rv = cur.fetchone()

        #rv = str(rv)
        val = int(rv[0])

        #return jsonify({"value " : val})
        if val > 0:
            return jsonify({"status" : "Failure" ,"message" : "User Name "+uname +" already exists"})
        else:
            cur.execute('''INSERT INTO users(user_name,password) values (%s , %s)''',(uname,passwd))
            mysql.connection.commit()
            return jsonify({"status" : "Success" , "message" : "User registration successful"})

class Login1(Resource):
    def get(self):
        auth = request.authorization
        #login_data = request.get_json()
        uname  = str(auth.username) #str(login_data['user_name'])
        passwd = str(auth.password) #str(login_data['password'])
        return jsonify({"Validated" : " User Name : "+uname +" Password :"+passwd})

class Login(Resource):
    def get(self):
                auth = request.authorization

                #login_data = request.get_json()
                uname  = str(auth.username) #str(login_data['user_name'])
                passwd = str(auth.password) #str(login_data['password'])

                #uname = str(login_data['user_name'])
                #passwd = str(login_data['password'])
                cur = mysql.connection.cursor()
                #sql = ('''SELECT COUNT(*) FROM USERS WHERE USER_NAME = %s AND PASSWORD = %s''',(uname,passwd))

                cur.execute('''SELECT COUNT(*) FROM USERS WHERE USER_NAME = %s AND PASSWORD = %s''',(uname,passwd))
                rv = cur.fetchone()
                valid_usr = int(rv[0])
                #valid_usr = int(valid_usr)

                if valid_usr > 0:
                    token = jwt.encode({"user":auth.username,"exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 600)}, app.config['SECRET_KEY'])
                    return jsonify({"status" : "Success" , "message": "successful login", "token" : token.decode('UTF-8' )})
                else:
                    sql = ("select count(*) from  Users where user_name = '"+uname+"'")
                    #cur.execute('''SELECT COUNT(*) FROM USERS WHERE USER_NAME = %s''',uname)
                    cur.execute(sql)
                    retval = cur.fetchone()
                    valid_usr1 = int(retval[0])
                    #return jsonify({"Status" : "Failure"})

                    if valid_usr1 < 1:
                        #return jsonify({"status" : "Failure", "message" : "Invalid User name"})
                        return make_response('Invalid User Name!',401,{'WWW-Authenticate':'Basic realm="Login Failed"'})
                    else:
                        #return jsonify({"status" : "Failure", "message" : "Password entered is Invalid"})
                        return make_response('Invalid Password!',401,{'WWW-Authenticate':'Basic realm="Login Failed"'})

class History(Resource):
        @token_required
        def get(self):
            return jsonify({"message" : "This is a private method"})
            #message = json.dumps({'errors': errors})
            #return Response(message, status=422, mimetype='application/json')
        #method_decorators = [authenticate]
#from .plots import ViewAllPlots
#class ViewAllPlots

class ViewAllPlots(Resource):
    @token_required
    def get(self):
        cur = mysql.connection.cursor()
        sql = ("select plot_id,plot_owner_id,plot_size,location_id from  Plots ")
        cur.execute(sql)
        plots = cur.fetchall()
        count = len(plots)
        data =''
        field1=''
        field2=''
        field3=''
        field4=''
        field5=''

        json ={}
        for index,plot in enumerate(plots):
            field1 =field1+','+str(plots[index][0])
            field2 = field2+','+str(plots[index][1])
            field3 = field3+','+str(plots[index][2])
            field4 = field4+','+str(plots[index][3])
            #field5 = field5+', '+str(plots[0][4])
            #field6 = field6+', '+str(plots[0][5])

        json= jsonify({"count" : str(count)+" Plots selected "
        ,"plot_id" : [field1]
        ,"plot_owner_id" : [field2]
        ,"plot_size" : [field3]
        ,"location_id" : [field4] #,"field5" : field5
        }) #plots

        return json

class addlocation(Resource):
    @token_required
    def post(self):
        auth = request.authorization
        username = str(auth.username)
        #fetch user_id
        user_id = get_user_id(username)

        location_id = create_owner_locations(user_id)

        #create owner_site
        owner_site_id = create_owner_site(user_id,location_id)


class PostProperty(Resource):
    @token_required
    def post(self):

        auth = request.authorization
        username = str(auth.username)
        cur = mysql.connection.cursor()

        #fetch user_id
        user_id = get_user_id(username)

        #get location
        #location_id = get_location(user_id)
        location_id = str(123) #int(1234)

        #add plots
        #add parkable sites


        #plot data
        data = request.get_json()

        plot_size  = str(data['plot_size'])
        #avialable  = data['availability']
        #quoted_amt = data['quote']
        cur.execute('''INSERT INTO Plots(plot_owner_id,plot_size,location_id) values (%s ,%s ,%s)''', (user_id,plot_size,location_id))
        #cur.execute('''INSERT INTO Plots(plot_owner_id,plot_size,location_id) values (%d,%s,%d)''',(user_id,plot_size,location_id))
        mysql.connection.commit()
        return jsonify({"message" : "Plot is added successfully", "plot_size" : plot_size, "user_id" : user_id , "location_id" : location_id})

#class Users(Resource):

api.add_resource(Home,'/')
api.add_resource(Register,'/register')
api.add_resource(Login,'/login')
api.add_resource(Login1,'/login1')
api.add_resource(History,'/history')
api.add_resource(PostProperty,'/addproperty')
api.add_resource(addlocation,'/addlocation')
api.add_resource(ViewAllPlots,'/viewplots')
api.add_resource(Signup, '/signup')
#api.add_resource(Users,'/getuser')

if __name__ == '__main__':
    app.run(debug=True)

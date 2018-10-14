from flask import Flask
app = Flask(__name__)

#home page clause
@app.route('/')
def index():
    return 'welcome to the app'

if __name__ == '__main__':
	app.run(debug=True)

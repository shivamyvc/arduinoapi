# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,jsonify,request,render_template,url_for
import json
from mydb import ard_db
from db_operation import arduino_database

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def home():
    return render_template("index.html")
@app.route('/fetch-data')
def get_data():
    conn=ard_db.my_db_connect()
    cur=conn.cursor()
    cur.execute("select * from users")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)
@app.route('/RFID_data',methods = ['POST','GET'],)
def RFID_read():
    if request.method == 'POST':
      rfid_data=str(request.args.get("RFID")).upper()
      return "OK"
@app.route('/add_user',methods=["POST","GET"])
def add_user():
    fullname='Sharad Yadav'
    ph_number='+918451833935'
    addr='Lower Parel'
    arduino_database.add_passenger_details(fullname=fullname, ph_number=ph_number, addr=addr)
    # user.add_passenger_details(passenger_id,fullname,ph_number,addr)
    return "OK"
@app.route('/add_luggage_details',methods=["POST","GET"])
def add_luggae_details():
    passenger_id=1124
    luggage_dec="Red American Tourister bag"
    rfid="D9EF9BA"
    arduino_database.add_luggage_details(passenger_id, luggage_dec, rfid)
    # user.add_passenger_details(passenger_id,fullname,ph_number,addr)
    return "Luggage Adde"
# main driver function
@app.route('/get_passenger',methods=["POST","GET"])
def get_passenger():
    if request.method == 'POST':
      rfid=str(request.args.get("RFID")).upper()
      data=arduino_database.get_passenger_phone(rfid)
    return data
# main driver function

if __name__ == '__main__':
	# run() method of Flask class runs the application
	# on the local development server.
	app.run()

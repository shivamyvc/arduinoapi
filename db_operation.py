import json
from mydb import ard_db
class arduino_database:

    def add_passenger_details(fullname,ph_number,addr):
        # print(passenger_id,fullname,ph_number,addr)
        conn=ard_db.my_db_connect()
        cur=conn.cursor()
        query='''INSERT INTO `users`( `fullname`, `ph_number`, `addr`) VALUES (%s,%s,%s)'''
        userdata=(fullname,ph_number,addr)
        cur.execute(query,userdata)
        conn.commit()
    def add_luggage_details(passenger_id,luggage_dec,rfid):
        # print(passenger_id,fullname,ph_number,addr)
        conn=ard_db.my_db_connect()
        cur=conn.cursor()
        query='''INSERT INTO `luggage_details`(`passenger_id`, `luggage_dec`, `rfid`) VALUES(%s,%s,%s)'''
        userdata=(passenger_id,luggage_dec,rfid)
        cur.execute(query,userdata)
        conn.commit()
    def get_passenger_phone(rfid):
        # print(passenger_id,fullname,ph_number,addr)
        conn=ard_db.my_db_connect()
        cur=conn.cursor()
        query=f"SELECT users.fullname,users.ph_number FROM `users` INNER JOIN luggage_details ON users.passenger_id=luggage_details.passenger_id and luggage_details.rfid=\"{rfid}\""
        cur.execute(query)
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        return json.dumps(json_data)
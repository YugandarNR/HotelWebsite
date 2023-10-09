from flask import Flask,render_template,request,redirect, url_for,session
from datetime import datetime
import sqlite3

app=Flask(__name__,static_url_path='/static')
app.secret_key='123456789'
conn = sqlite3.connect('website_data.db',check_same_thread=False)
c = conn.cursor()

#Create Database Tables if they do not exist
#Create customers Table
c.execute('''CREATE TABLE IF NOT EXISTS Customers (CustomerId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15))''')
#Create retaurants table
c.execute('''CREATE TABLE IF NOT EXISTS Hotels (HotelId INTEGER PRIMARY KEY AUTOINCREMENT, HotelName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15))''')
conn.commit()

CUSTOMER_INFO="SELECT * FROM Customers WHERE Phone = ? AND Password = ?"
HOTEL_INFO="SELECT * FROM Hotels WHERE Phone = ? AND Password = ?"
REGISTER_CUSTOMER_ENTRY="INSERT INTO Customers VALUES (NULL,?,?,?,?,?,?,?,?)"
REGISTER_HOTEL_ENTRY="INSERT INTO Hotels VALUES (NULL,?,?,?,?,?,?,?,?)"

@app.route('/',methods=['POST','GET'])
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        phone = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        #Get Customer Name if Customer is logging in
        if user_type == 'Customer':
            c.execute(CUSTOMER_INFO, (phone, password))
        #Get Restaurant Name if Restaurant is logging in
        else:
            c.execute(HOTEL_INFO, (phone, password))
        account=c.fetchone()
        conn.commit()
        if account:
            session['loggedin'] = True
            session['username'] = account[1]
            #Render user_home.html if user is logging in
            if user_type == 'Customer':
                session['UserId'] = account[0]
                return redirect("user_home")
            #Render restaurant_home.html with restaurant name if restaurant is logging in
            else:
                session['RestId'] = account[0]
                return redirect("/hotel_home")
        # if no account is found say Incorrect ID / Pass
        else:
            return render_template('login.html',msg= "Incorrect Phone Number/Password")
    return render_template ('login.html')
#Register Page
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        user_type=request.form['user_type']
        name = request.form['name']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #Insert user only if both passwords match
        if password == confirm_password:
            #If user_type is customer add user info to customers table
            if user_type == 'Customer':
                c.execute(REGISTER_CUSTOMER_ENTRY,(name,phone,street,city,state,pincode,email,password))
            #If user_type is Restaurant add info to restarurants table
            else:
                if delivery_fee:
                    c.execute(REGISTER_HOTEL_ENTRY,(name,phone,street,city,state,pincode,email,password))
                else:
                    return render_template('register.html',msg="Delivery Fee is required")
        #If passwords do not match
        else:
            return render_template('register.html',msg="Both Passwords do not match")
        conn.commit()
        return render_template ('login.html')
    return render_template ('register.html')

if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)

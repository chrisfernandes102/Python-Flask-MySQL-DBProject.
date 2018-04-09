from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from contextlib import closing


mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'qvmwCIUYFaNvllDlpccKkuBgJge9fXmDmV70JoS+'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'flask'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chriselise2'
app.config['MYSQL_DATABASE_DB'] = 'VehicleDB'
app.config['MYSQL_DATABASE_HOST'] = 'dbproject.czooch6gy5ll.us-east-2.rds.amazonaws.com'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/adminHome')
def adminHome():
    if session.get('user'):
        return render_template('adminHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/showSalesperson')
def showSalesperson():
    if session.get('user'):
        return render_template('salesperson.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/showSearch')
def search():
    if session.get('user'):
        return render_template('search.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/showUpdate')
def update():
    if session.get('user'):
        return render_template('update.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/showSales')
def sales():
    if session.get('user'):
        return render_template('sales.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/addCar')
def car():
    if session.get('user'):
        return render_template('Car.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['Username']
        _password = request.form['Password']

        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM Salesperson WHERE Username = %s AND Password = %s"
        parameter = (_username, _password)
        cursor.execute(query, parameter)
        data = cursor.fetchall()

        con = mysql.connect()
        cursor = con.cursor()
        query2 = "SELECT * FROM Admin WHERE Username = %s AND Password = %s"
        parameter2 = (_username, _password)
        cursor.execute(query2, parameter2)
        data2 = cursor.fetchall()

        if len(data) > 0:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    if str(data[0][4]) == _password:
                        session['user'] = data[0][3]
                        return redirect('/userHome', session['user'])
                    else:
                        return render_template('error.html', error='Wrong Email address or Password.')

        elif len(data2) > 0:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    if str(data2[0][4]) == _password:
                        session['user'] = data2[0][3]
                        return redirect('/adminHome', session['user'])
                    else:
                        return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')


    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['FirstName']
        _lastname = request.form['LastName']
        _username = request.form['Username']
        _password = request.form['Password']
        _hashed_password = generate_password_hash(_password)

        # validate the received values
        if _name and _lastname and _username and _password:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "INSERT INTO Salesperson (FirstName, LastName, Username, Password) VALUES(%s,%s, %s, %s)"
                    parameter = (_name, _lastname, _username, _password)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()

                    if len(data) is 0:
                        conn.commit()
                        return json.dumps({'message': 'User created successfully !'})
                    else:
                        return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/showSearch', methods=['POST', 'GET'])
def searchCar():
    try:
        _VIN = request.form['VIN']
        _Make = request.form['Make']
        _Model = request.form['Model']
        _Year = request.form['Year']
        _Color = request.form['Color']

        # validate the received values
        if _VIN:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT * FROM Car WHERE VIN = %s"
                    parameter = (_VIN)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('found.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Vehicle')
        elif _Make:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT * FROM Car WHERE Make = %s"
                    parameter = (_Make)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('found.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Vehicle')
        elif _Model:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT * FROM Car WHERE Model = %s"
                    parameter = (_Model)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('found.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Vehicle')
        elif _Year:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT * FROM Car WHERE Year = %s"
                    parameter = (_Year)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('found.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Vehicle')
        elif _Color:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT * FROM Car WHERE Color = %s"
                    parameter = (_Color)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('found.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Vehicle')
        else:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT * FROM Car"
                    cursor.execute(query)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('found.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Vehicle')

    except Exception as e:
        return json.dumps({'error': str(e)})



@app.route('/showSalesSearch', methods=['POST', 'GET'])
def searchSales():
    try:
        _CustomerFirstName = request.form['CustomerFirstName']
        _CustomerLastName = request.form['CustomerLastName']
        _SalespersonFirstName = request.form['SalespersonFirstName']
        _SalespersonLastName = request.form['SalespersonLastName']
        _VIN = request.form['VIN']

        # validate the received values
        if _CustomerFirstName:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT SalesInvoice.InvoiceID, SalesInvoice.InvoiceNumberDate, Customer.FirstName, Customer.LastName, " \
                            "Car.Make, Car.Model, Salesperson.FirstName, Salesperson.LastName " \
                            "FROM SalesInvoice " \
                            "JOIN Customer ON SalesInvoice.CustomerID=Customer.CustomerID " \
                            "JOIN Salesperson ON SalesInvoice.SalespersonID=Salesperson.SalespersonID " \
                            "JOIN Car ON SalesInvoice.VIN=Car.VIN WHERE Customer.FirstName=%s"
                    parameter = _CustomerFirstName
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('foundSales.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Invoice')
        elif _CustomerLastName:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT SalesInvoice.InvoiceID, SalesInvoice.InvoiceNumberDate, Customer.FirstName, Customer.LastName, " \
                            "Car.Make, Car.Model, Salesperson.FirstName, Salesperson.LastName " \
                            "FROM SalesInvoice " \
                            "JOIN Customer ON SalesInvoice.CustomerID=Customer.CustomerID " \
                            "JOIN Salesperson ON SalesInvoice.SalespersonID=Salesperson.SalespersonID " \
                            "JOIN Car ON SalesInvoice.VIN=Car.VIN WHERE Customer.LastName=%s"
                    parameter = _CustomerLastName
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('foundSales.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Invoice')
        elif _SalespersonFirstName and _SalespersonLastName:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT SalesInvoice.InvoiceID, SalesInvoice.InvoiceNumberDate, Customer.FirstName, Customer.LastName, " \
                            "Car.Make, Car.Model, Salesperson.FirstName, Salesperson.LastName " \
                            "FROM SalesInvoice " \
                            "JOIN Customer ON SalesInvoice.CustomerID=Customer.CustomerID " \
                            "JOIN Salesperson ON SalesInvoice.SalespersonID=Salesperson.SalespersonID " \
                            "JOIN Car ON SalesInvoice.VIN=Car.VIN WHERE Salesperson.FirstName=%s AND Salesperson.LastName=%s"
                    parameter = (_SalespersonFirstName,_SalespersonLastName)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('foundSales.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Invoice')
        elif _VIN:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT SalesInvoice.InvoiceID, SalesInvoice.InvoiceNumberDate, Customer.FirstName, Customer.LastName, " \
                            "Car.Make, Car.Model, Salesperson.FirstName, Salesperson.LastName " \
                            "FROM SalesInvoice " \
                            "JOIN Customer ON SalesInvoice.CustomerID=Customer.CustomerID " \
                            "JOIN Salesperson ON SalesInvoice.SalespersonID=Salesperson.SalespersonID " \
                            "JOIN Car ON SalesInvoice.VIN=Car.VIN WHERE Car.VIN=%s"
                    parameter = _VIN
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()
                    print(data)
                    if len(data):
                        return render_template('foundSales.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Invoice')
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/showSalesUpdate', methods=['POST', 'GET'])
def updateSalesInvoice():
    try:
        _Vin = request.form['VIN']
        _Date = request.form['Date']
        _CustomerFirstName = request.form['CustomerFirstName']
        _CustomerLastName = request.form['CustomerLastName']
        _SalespersonFirstName = request.form['SalespersonFirstName']
        _SalespersonLastName = request.form['SalespersonLastName']

        # validate the received values
        if _CustomerFirstName and _CustomerLastName and _SalespersonFirstName and _SalespersonLastName and _Vin:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query1 = "SELECT * FROM Customer WHERE FirstName=%s AND LastName=%s"
                    parameter = (_CustomerFirstName, _CustomerLastName)
                    cursor.execute(query1, parameter)
                    data = cursor.fetchall()
                    conn.commit()

                    query2 = "SELECT * FROM Salesperson WHERE FirstName=%s AND LastName=%s"
                    parameter2 = (_SalespersonFirstName, _SalespersonLastName)
                    cursor.execute(query2, parameter2)
                    data2 = cursor.fetchall()
                    conn.commit()

                    query3 = "INSERT INTO SalesInvoice(InvoiceNumberDate, CustomerID, VIN, SalespersonID) VALUES ('%s', %s, '%s', %s)" % (_Date, data[0][0], _Vin, data2[0][0])
                    cursor.execute(query3)
                    data3 = cursor.fetchall()
                    conn.commit()

                    query5 = "UPDATE Car SET SalesPersonID=%s AND CarForSale=0 WHERE VIN='%s'" % (data2[0][0], _Vin)
                    cursor.execute(query5)
                    conn.commit()

                    query4 = "SELECT * FROM SalesInvoice WHERE VIN='%s'" % (_Vin)
                    cursor.execute(query4)
                    data4 = cursor.fetchall()
                    conn.commit()

                    if len(data4):
                        return render_template('success.html', data="Sales Invoice was made successfully.")
                    else:
                        return render_template('error.html', error='Could not find Invoice')

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/showCarAdd', methods=['POST', 'GET'])
def carAdd():
    try:
        _Vin = request.form['VIN']
        _Make = request.form['Make']
        _Model = request.form['Model']
        _Year = request.form['Year']
        _Color = request.form['Color']
        _Mileage = request.form['Mileage']
        _RetailPrice = request.form['RetailPrice']
        _NewOrUsed = request.form['NewOrUsed']

        # validate the received values
        if _Vin and _Make and _Model and _Year and _Color and _Mileage and _RetailPrice and _NewOrUsed:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # All Good, let's call MySQL
                    conn = mysql.connect()
                    cursor = conn.cursor()

                    if _NewOrUsed == 'New':
                        query1 = "INSERT INTO Car(VIN, Make, Model, Year, RetailPrice, CarForSale, Color, Mileage, NewOrUsed) VALUES " \
                             "('%s', '%s', '%s', %s, %s, %s,'%s', %s, %s)" % (_Vin, _Make, _Model, _Year, _RetailPrice, 1, _Color, _Mileage, 1)
                        cursor.execute(query1)
                        conn.commit()
                    elif _NewOrUsed == 'Used':
                        query1 = "INSERT INTO Car(VIN, Make, Model, Year, RetailPrice, CarForSale, Color, Mileage, NewOrUsed) VALUES " \
                                 "('%s', '%s', '%s', %s, %s, %s, '%s', %s, %s)" % (_Vin, _Make, _Model, _Year, _RetailPrice, 1, _Color, _Mileage, 0)
                        cursor.execute(query1)
                        conn.commit()

                    query2 = "SELECT * FROM Car WHERE VIN='%s'" % (_Vin)
                    cursor.execute(query2)
                    data4 = cursor.fetchall()
                    conn.commit()

                    if len(data4):
                        return render_template('success.html', data="The Car was successfully added.")
                    else:
                        return render_template('error.html', error='Could not add Vehicle')

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/showSalesPerson', methods=['GET', 'POST'])
def salesperson():
    try:
        _SalespersonFirstName = request.form['SalespersonFirstName']
        _SalespersonLastName = request.form['SalespersonLastName']


        if _SalespersonFirstName and _SalespersonLastName:
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    # connect to mysql

                    con = mysql.connect()
                    cursor = con.cursor()
                    query = "SELECT * FROM Salesperson WHERE FirstName = %s AND LastName = %s"
                    parameter = (_SalespersonFirstName, _SalespersonLastName)
                    cursor.execute(query, parameter)
                    data = cursor.fetchall()

                    if str(data):
                        return render_template('foundSalesPerson.html', data=data)
                    else:
                        return render_template('error.html', error='Could not find Sales Person')
        else:
            # connect to mysql
            con = mysql.connect()
            cursor = con.cursor()
            query = "SELECT * FROM Salesperson"
            cursor.execute(query)
            data = cursor.fetchall()

            if str(data):
                return render_template('foundSalesPerson.html', data=data)
            else:
                return render_template('error.html', error='Could not find Sales Person')


    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
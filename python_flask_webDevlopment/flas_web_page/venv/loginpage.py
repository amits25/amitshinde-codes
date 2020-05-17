#####################################################################

	#Author :: Amit Shinde
	#DESC:: Sample web- Devlopement code with python flask module

#####################################################################

from flask import Flask, render_template, redirect, url_for, request
import os
from http import cookies
import sqlite3
import base64
#import nexmo
#from twilio import twiml
from werkzeug import secure_filename
app = Flask(__name__, template_folder='template')
PEOPLE_FOLDER = os.path.join('static', 'Images')
app.config['Images'] = PEOPLE_FOLDER
C = cookies.SimpleCookie();


def DB():
    global conn, cursor
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor()


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/home')
def home():
    C.clear()
    #print(C.output("username"))
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = None

    if request.method == 'POST':
        DB()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?",
                       (request.form['username'], request.form['password']))
        if cursor.fetchone() is not None:
            if request.form['username']=="admin":
                C["username"] = request.form['username']
                print(C.output("username"))
                conn.commit()
                conn.close()
                '''resp = make_response(render_template('admin.html', username=request.form['username']))
                resp.set_cookie('somecookiename', 'I am cookie')
                return resp'''
                return render_template('admin.html', username=request.form['username'])
            else:
                C["username"] = request.form['username']
                conn.commit()
                conn.close()
                return render_template('home.html', username=request.form['username'])

        else:
             cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
             conn.commit()
             error = 'Invalid Credentials. Please try again.'
             conn.close()
             return render_template('login.html', error=error)

    else:
         return render_template('login.html')


@app.route('/reg1', methods=['POST', 'GET'])
def reg():
    error = None
    var=None
    var1=None
    uname=None
    if request.method == 'POST':
        DB()
        if "empty" != request.form['password']:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
            cursor.execute("INSERT INTO `member` (username, password) VALUES( ?,?)",
                           (request.form['username'], request.form['password']))
            conn.commit()
            conn.close()
            error = 'Registration successfull please login.'
            return render_template('login.html', error=error)

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?",
                       (request.form['username'],))
        if cursor.fetchone() is None:
            name=request.form['username']
            print(name)
            error = 'username is available'
            return render_template('registration123.html', var=1, error=error, uname=name)
        else:  # on failed Reg.
            error = 'username allready exits please try another username or try to login.'
            return render_template('registration123.html', var1=1, error=error)
    else:
        return render_template('registration123.html', var1=1)


@app.route('/backtologin')
def BackToLoginPage():
    return render_template('login.html')


@app.route('/adminfun')
def adminfunctions():
    row = None
    DB()
    cursor.execute("SELECT * FROM `member`")
    rows = cursor.fetchall()
    conn.close()
    return render_template('showall.html', row=rows)


@app.route('/backtoadmin')
def BAckToadminfunctions():
    username = None
    return render_template('admin.html', username="Admin")


@app.route('/deleteThis', methods=['POST', 'GET'])
def deletefromdb():
    if request.method == 'POST':
        error = None
        DB()
        data = request.form['val']
        #print(data)
        cursor.execute("DELETE FROM `member` WHERE `username` = ?", (request.form['val'],))
        conn.commit()
        cursor.execute("SELECT * FROM `member`")
        rows = cursor.fetchall()
        error = "row deleted successfully"
        conn.close()
        return render_template('showall.html', row=rows, error=error)


@app.route('/updtaerow', methods=['POST', 'GET'])
def updatetodb():
    if request.method == 'POST':
        DB()
        error = None
        print("hello")
        data = request.form['vall']
        print(data)
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? ",
                       (request.form['vall'],))
        rows = cursor.fetchone()
        error="update the contains"
        conn.close()
        return render_template('admin/update.html', row=rows, error=error)


@app.route('/updtaerow2', methods=['POST', 'GET'])
def updatetodb2():
    if request.method == 'POST':
        DB()
        sql_update_query = """Update member set password = ? where username = ?"""
        data = (request.form['password'], request.form['username'])
        cursor.execute(sql_update_query, data)
        conn.commit()
        cursor.execute("SELECT * FROM `member`")
        rows = cursor.fetchall()
        error = "Updated successfully"
        conn.close()
        return render_template('showall.html', row=rows, error=error)



@app.route('/uploadImg', methods=['GET','POST'])
def UploadImages():
    if request.method == 'POST':
        DB()
        row=None
        file = request.files['fileToUpload']
        filename = secure_filename(file.filename)
        full_filename = os.path.join(app.config['Images'], filename)
        file.save(full_filename)
        print(full_filename)
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `carsImg` (car_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, name TEXT)")
        cursor.execute("INSERT INTO `carsImg` (name) VALUES( ?)",
                       (full_filename,))
        conn.commit()
        cursor.execute("SELECT * FROM `carsImg`")
        rows = cursor.fetchall()
        print(rows)
        conn.close()
        return render_template('Images/showAllCars.html', row=rows)


@app.route('/showIMG', methods=['GET'])
def UploadImagesPage():
    DB()
    row=None
    cursor.execute("SELECT * FROM `carsImg`")
    rows = cursor.fetchall()
    print(rows)
    conn.close()
    return render_template('Images/showAllCars.html', row=rows)


@app.route('/deleteIMG', methods=['POST'])
def DeleteIMGFromDB():
    if request.method == 'POST':
        DB()
        error = None
        print("hello")
        data = request.form['vall']
        print(data)
        data1="/home/kpit/PycharmProjects/login1/venv/"+data
        print(data1)
        os.remove(data1)
        cursor.execute("DELETE FROM `carsImg` WHERE `name` = ?", (data,))   #query form
        conn.commit()
        error1="IMG deleted siccessfully"
        cursor.execute("SELECT * FROM `carsImg`")
        rows = cursor.fetchall()
        print(rows)
        conn.close()
        return render_template('Images/showAllCars.html', row=rows, error=error1)


@app.route('/userIMG', methods=['GET'])
def showIMGtouser():
    DB()
    row=None
    cursor.execute("SELECT * FROM `carsImg`")
    rows = cursor.fetchall()
    print(rows)
    conn.close()
    return render_template('Images/userImg.html',row=rows)


@app.route('/uploadimage', methods=['GET'])
def pagetouploadIMG():
    return render_template('Images/uploadImg.html')


@app.route('/backtouser', methods=['GET'])
def backtoadminpage():
    username=None
    name=C.output("username")
    print(name)
    uname=name.split("=")
    Uname=uname[1]
    print(Uname)
    return render_template('home.html',username=Uname)


@app.route('/dropdown', methods=['GET'])
def DropDownList():
    DB()
    row=None
    cursor.execute("SELECT * FROM `carsImg`")
    rows = cursor.fetchall()
    print(rows)
    conn.close()
    return render_template('Images/dropdown.html',row=rows)


@app.route('/toIMG')
def DropDownListToIMG():
    DB()
    row=None
    row1=None
    post_id = request.args.get('name')
    print(post_id)
    cursor.execute("SELECT * FROM `carsImg`")
    rows = cursor.fetchall()
    print(rows)
    query = "SELECT * FROM carsImg WHERE car_id = {};".format(post_id)
    cursor.execute(query)
    rows1 = cursor.fetchall()
    print(rows1)
    conn.close()
    return render_template('Images/dropdown.html', row=rows, row1=rows1)


@app.route('/specificIMG')
def ToSpecificCAr():
    DB()
    post_id = request.args.get('id')
    row=None
    query = "SELECT * FROM carsImg WHERE car_id = {};".format(post_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return render_template('Images/specificCar.html', row=rows)


'''@app.route('/reg', methods=['POST', 'GET'])
def reg1():
    error = None
    if request.method == 'POST':
        DB()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?",
                       (request.form['username'],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `member` (username, password) VALUES( ?,?)", (request.form['username'], request.form['password']))
            conn.commit()
            conn.close()
            error = 'Registration successfull please login.'
            return render_template('login.html',  error=error)
        else:  # on failed Reg.
            error = 'Registration Not successfull username already exits.'
            return render_template('registration.html', error=error)
    else:
        return render_template('registration.html')'''


@app.route('/sms', methods=['GET'])
def smssend():
    client = nexmo.Client(key='40bb4a91', secret='UWIfTY9qsRM06atx')

    client.send_message({
        'from': 'Nexmo',
        'to': '100',
        'text': 'Hello from Nexmo',
    })

if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(debug=True, host='localhost', port=8085)


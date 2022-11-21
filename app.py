from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
 
app = Flask(__name__)
       
app.secret_key = "caircocoders-ednalan"
       
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sfdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
 
@app.route('/')
def index():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM tblstudent ORDER BY idno")
    student = cur.fetchall()
    return render_template('index.html', student=student)
 
@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        txtidno = request.form['txtidno']
        txtname = request.form['txtname']
        txtcourse = request.form['txtcourse']
        txtlevel = request.form['txtlevel']
        print(txtname)
        if txtidno == '':
            msg = 'Please Input idno'  
        elif txtname == '':
           msg = 'Please Input name'  
        elif txtcourse == '':
           msg = 'Please Input course'  
        elif txtlevel == '':
           msg = 'Please Input level'
        else:        
            cur.execute("INSERT INTO tblstudent(idno,name,course,level) VALUES (%s,%s,%s,%s)",[txtidno,txtname,txtcourse,txtlevel])
            mysql.connection.commit()       
            cur.close()
            msg = 'New record created successfully'   
    return jsonify(msg)
 
 
     
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask,render_template,request,flash,redirect,session
from dbhelper import*

app = Flask(__name__)
app.secret_key="@#$klarke"

@app.route("/savestudent",methods=['POST'])
def savestudent():
    idno: str = request.form["idno"]
    name: str = request.form["name"]
    course: str = request.form["course"]
    level: str = request.form["level"]
    
    #
    if idno!=None and name!=None:
        okey: bool=addrecord('tblstudent',idno=idno,name=name,course=course,level=level)
        if okey:
            flash("New Student Added")
            return redirect("/main")

@app.route("/deletestudent")
def deletestudent():
    idnumber: str = request.args.get("idno")
    okey: bool= deleterecord('tblstudent',idno=idnumber)
    if okey:
        flash("Student Deleted")
        return redirect("/main")
    else:
        flash("Error Deleting Student")
        return redirect("/main")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"]="no-chache,no-store,must-revalidate"
    return response

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out")
    return redirect("/")

@app.route("/main")
def main():
    if "logged_user" in session:
        header: list=['idno','name','course','level','action']
        stlist:list = getallrecord('tblstudent')
        return render_template("main.html",headername='student list',studentlist=stlist,head=header)
    else:
        flash("Login Properly!")
        return redirect("/")  

@app.route("/login", methods=['POST'])
def login():
    uname: str=request.form["username"]
    pword: str=request.form["password"]
    user: dict=userlogin('users',username=uname,password=pword)
    if user !=None:
        session["logged_user"]=user["username"]
        flash("Login Accepted")
        return redirect("/main")
    else:
        flash("Login Failed")
        return redirect("/")

@app.route("/")
def index():
    return render_template("login.html",headername='user login')

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)

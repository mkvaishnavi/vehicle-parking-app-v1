from flask import Flask , render_template , request , redirect , session
import sqlite3

app=Flask(__name__)
app.secret_key="secret_key_123"
@app.route("/Register",methods=["GET","POST"])
def registration():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        full_name=request.form["full_name"]
        username=request.form["username"]
        password=request.form["password"]
        email=request.form["email"]
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("""INSERT INTO User (full_Name, email, username, password, role) VALUES (?, ?, ?,?, 'user')""", (full_name, email, username, password))

        connection.commit()
        connection.close()
    return "Registration Successful"

@app.route("/Login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM User WHERE email=? AND password=?",(email,password))
        user=cursor.fetchone()
        connection.close()
        if user:
            role=user[5]
            session["username"]=user[1]
            session["role"]=user[5]
            if role == "admin":
                return redirect("/admin_dashboard")
            else:
                return redirect("/user_dashboard")
        else:
            return render_template("login.html", error="Invalid Credentials")

@app.route("/user_dashboard")
def user_dashboard():
    if "username" not in session or session["role"]!="user":
        return redirect("/Login")
    return render_template("user_dashboard.html",username=session["username"])

@app.route("/admin_dashboard")
def admin_dashboard():
    if "username" not in session or session["role"]!="admin":
        return redirect("/Login")
    return render_template("admin_dashboard.html",username=session["username"])

@app.route("/Logout")
def logout():
    session.clear()
    return redirect("/Login")

if __name__=="__main__":
    app.debug=True
    app.run()

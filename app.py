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
        address=request.form["address"]
        pincode=request.form["pincode"]
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("""INSERT INTO User (full_Name, email, username, password, address, pincode, role) VALUES (?,?,?,?,?,?,'user')""", (full_name, email, username, password,address,pincode))

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
            role=user[7]
            session["username"]=user[1]
            session["role"]=user[7]
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
    else:
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Parking_Lots")
        lots=cursor.fetchall()
        connection.close()
        return render_template("admin_dashboard.html", lots=lots)

@app.route("/Logout")
def logout():
    session.clear()
    return redirect("/Login")

@app.route("/Add_Lot",methods=["GET","POST"])
def add_lot():
    if request.method=="GET":
        return render_template("add_lot.html")
    if request.method=="POST":
        Location=request.form["Location"]
        Address=request.form["Address"]
        Pincode=request.form["Pincode"]
        Price=request.form["Price"]
        Spots=int(request.form["Spots"])
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("""INSERT INTO Parking_Lots(Location_name,Price,Address,Pincode,no_of_spots) VALUES(?,?,?,?,?)""", (Location,Price,Address,Pincode,Spots))
        lot_id=cursor.lastrowid
        for i in range(int(Spots)):
            cursor.execute("""INSERT INTO Parking_spots(Lot_ID,status) VALUES(?,?)""",(lot_id,"A"))
        connection.commit()
        connection.close()
        return redirect("/admin_dashboard")
    
@app.route("/View_Lot/", methods=["GET"])
def view_lot():
    lot_id=request.args.get("lot_id")
    if not lot_id:
        return render_template("view_lot.html",lot=None)
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM Parking_Lots WHERE Lot_ID=?", (lot_id,))
    lot=cursor.fetchone()
    cursor.execute("SELECT * FROM Parking_spots WHERE Lot_ID=?", (lot_id,))
    spots=cursor.fetchall()
    connection.close()
    return render_template("view_lot.html", lot=lot,spots=spots)

@app.route("/View_Spot/",methods=["GET","POST"])
def view_spots(spot_id):
    if request.method == "GET":
        return render_template("view_spots.html", spots=None)
    if request.method == "POST":
        spot_id = request.form["spot_id"]
        if not spot_id:
            return render_template("view_spots.html", spots=None, spot_id=None)
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Parking_spots WHERE Spot_ID=?", (spot_id,))
        spots = cursor.fetchall()
        connection.close()
        return render_template("view_spots.html", spots=spots, spot_id=spot_id)
    
@app.route("/Edit_Lot/<int:lot_id>",methods=["GET","POST"])
def edit_lot(lot_id):
    if request.method == "GET":
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Parking_Lots WHERE Lot_ID=?", (lot_id,))
        lot=cursor.fetchone()
        connection.close()
        return render_template("edit_lot.html",lot=lot)
    if request.method == "POST":
        lot_id = request.form["lot_id"]
        Location=request.form["Location"]
        Address=request.form["Address"]
        Pincode=request.form["Pincode"]
        Price=request.form["Price"]
        Spots=request.form["Spots"]
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute(""" UPDATE Parking_Lots SET Location_name=?,Price=?,address=?,Pincode=?,no_of_spots=? WHERE Lot_ID=?""", (Location,Price,Address,Pincode,Spots,lot_id))
        connection.commit()
        connection.close()
        return redirect("/admin_dashboard")
    
@app.route("/Delete_Lot", methods=["POST"])
def delete_lot():
    lot_id=request.form["lot_id"]
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM Parking_spots WHERE Lot_ID=? AND status='O'",(lot_id,))
    occupied_spots=cursor.fetchall()
    if occupied_spots:
        connection.close()
        return "<p>Cannot delete lot with occupied spots.</p><a href='/admin_dashboard'>Go back</a>"
    cursor.execute("DELETE FROM Parking_spots WHERE Lot_ID=?", (lot_id,))
    cursor.execute("DELETE FROM Parking_Lots WHERE Lot_ID=?", (lot_id,))
    connection.commit()
    connection.close()
    return redirect("/admin_dashboard")

@app.route("/View_Users", methods=["GET"])
def view_users():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM User WHERE role='user'")
    users = cursor.fetchall()
    connection.close()
    return render_template("view_users.html", users=users)

if __name__=="__main__":
    app.debug=True
    app.run()

from flask import Flask , render_template , request , redirect , session
from datetime import datetime 
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
            session["user_id"]=user[0]
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
    user_id=session["user_id"]
    username=session["username"]
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("SELECT DISTINCT pl.* FROM Parking_Lots pl JOIN Parking_spots ps ON pl.Lot_ID=ps.Lot_ID WHERE ps.status='A'")
    available_lots=cursor.fetchall()
    cursor.execute("""SELECT r.Reservation_ID, r.Spot_ID, r.Vehicle_number, r.Parking_time, ps.Lot_ID, pl.Price FROM Reservations r JOIN Parking_spots ps ON r.Spot_ID = ps.Spot_ID JOIN Parking_Lots pl ON ps.Lot_ID = pl.Lot_ID WHERE r.User_ID = ? AND r.Leaving_time IS NULL ORDER BY r.Reservation_ID DESC LIMIT 1""", (user_id,))
    active_reservation = cursor.fetchone()
    connection.close()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("user_dashboard.html",username=username,lots=available_lots,current_time=current_time,reservation=active_reservation)

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

@app.route("/View_Spot/<int:spot_id>",methods=["GET","POST"])
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

@app.route("/Reserve_spot/<int:lot_id>", methods=["POST"])
def reserve_spot(lot_id):
    if "user_id" not in session:
        return redirect("/Login")
    user_id=session["user_id"]
    vehicle_number=request.form["vehicle_number"]
    lot_id=request.form["lot_id"]
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("""SELECT Spot_ID FROM Parking_spots WHERE Lot_ID=? AND status='A' ORDER BY Spot_ID ASC LIMIT 1""",(lot_id,))
    result=cursor.fetchone()
    if not result:
        connection.close()
        return "<p>No available spots in this lot.</p><a href='/user_dashboard'>Go back</a>"
    spot_id=result[0]
    parking_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    leaving_time=None
    parking_cost=None
    cursor.execute("""INSERT INTO Reservations (Spot_ID,User_ID,Vehicle_number,Parking_time,Leaving_time,Parking_cost) VALUES (?, ?, ?, ?,?,?)""", (spot_id,user_id,vehicle_number,parking_time,leaving_time,parking_cost))
    cursor.execute("""UPDATE Parking_spots SET status='O' WHERE Spot_ID=?""", (spot_id,))
    connection.commit()
    connection.close()
    return redirect("/user_dashboard")

@app.route("/Release_spot/<int:Spot_ID>", methods=["POST"])
def release_spot(Spot_ID):
    if "user_id" not in session:
        return redirect("/Login")
    user_id=session["user_id"]
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("""SELECT Reservation_ID , Parking_time FROM Reservations WHERE Spot_ID=? AND User_ID=? AND Leaving_time IS NULL""", (Spot_ID,user_id))
    row = cursor.fetchone()
    if row:
        reservation_id , parking_time = row[0], row[1]
        leaving_time = datetime.now()
        parking_time = datetime.strptime(parking_time, "%Y-%m-%d %H:%M:%S")
        parking_duration = (leaving_time - parking_time)
        cursor.execute("""UPDATE Reservations SET Leaving_time = ? WHERE Reservation_ID = ?""", (leaving_time.strftime("%Y-%m-%d %H:%M:%S"), reservation_id))
        cursor.execute("""UPDATE Parking_spots SET status = 'A' WHERE Spot_ID = ?""", (Spot_ID,))
    connection.commit()
    connection.close()
    return redirect("/user_dashboard",parking_duration=parking_duration)

@app.route("/user_history")
def user_history():
    if "user_id" not in session:
        return redirect("/Login")
    user_id = session["user_id"]
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT r.Reservation_ID, r.Spot_ID, r.Vehicle_number, r.Parking_time, r.Leaving_time, r.Parking_cost FROM Reservations r JOIN Parking_spots ps ON r.Spot_ID = ps.Spot_ID JOIN Parking_Lots pl ON ps.Lot_ID = pl.Lot_ID WHERE r.User_ID = ? ORDER BY r.Reservation_ID DESC""", (user_id,))
    history = cursor.fetchall()
    connection.close()
    history_with_duration = []
    for res in history:
        parking_time = datetime.strptime(res[3], "%Y-%m-%d %H:%M:%S")
        leaving_time = datetime.strptime(res[4], "%Y-%m-%d %H:%M:%S") if res[4] else None
        duration = str(leaving_time - parking_time) if leaving_time else "Still Parked"
        history_with_duration.append(res + (duration,))
    return render_template("user_history.html", history=history_with_duration)

@app.route("/all_parking_records")
def all_parking_records():
    if "role" not in session or session["role"]!="admin":
        return redirect("/Login")
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("""SELECT r.Reservation_ID , u.full_name , r.vehicle_number , r.parking_time , r.leaving_time , r.parking_cost , ps.Spot_ID , pl.Location_name FROM Reservations r JOIN User u ON r.User_ID = u.User_ID JOIN Parking_spots ps ON r.Spot_ID = ps.Spot_ID JOIN Parking_Lots pl ON ps.Lot_ID = pl.Lot_ID ORDER BY r.Reservation_ID DESC""")
    records=cursor.fetchall()
    connection.close()
    records_with_duration = []
    for r in records:
        parking_time = datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S")
        leaving_time = datetime.strptime(r[4], "%Y-%m-%d %H:%M:%S") if r[4] else None
        duration = str(leaving_time - parking_time) if leaving_time else "Still Parked"
        records_with_duration.append(r + (duration,))
    return render_template("all_parking_records.html",records=records_with_duration)

if __name__=="__main__":
    app.debug=True
    app.run()

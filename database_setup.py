import sqlite3
connection=sqlite3.connect('database.db')
cursor=connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""CREATE TABLE User(
        user_ID INTEGER PRIMARY KEY,
        username TEXT,
        email VARCHAR,
        password VARCHAR,
        full_name TEXT,
        address TEXT,
        pincode INTEGER,
        role TEXT
    );
""")
cursor.execute("""CREATE TABLE Parking_Lots(
        Lot_ID INTEGER PRIMARY KEY,
        Location_name TEXT,
        Price INTEGER,
        Address TEXT,
        Pincode INTEGER,
        no_of_spots INTEGER
    );
""")
cursor.execute("""CREATE TABLE Parking_spots(
        Spot_ID INTEGER PRIMARY KEY,
        Lot_ID INTEGER,
        status TEXT,
        FOREIGN KEY (Lot_ID) REFERENCES Parking_Lots(Lot_ID)
    );
""")
cursor.execute("""CREATE TABLE Reservations(
        Reservation_ID INTEGER PRIMARY KEY,
        Spot_ID INTEGER,
        User_ID INTEGER,
        Parking_time TEXT,
        Leaving_time TEXT,
        Parking_cost INTEGER,
        FOREIGN KEY (Spot_ID) REFERENCES Parking_spots(Spot_ID),
        FOREIGN KEY (User_ID) REFERENCES User(User_ID)
    );
""")
cursor.execute("""INSERT INTO User(username,email,password,full_name,address,pincode,role) VALUES(?,?,?,?,?,?,?)""", ("admin","admin@gmail.com","admin123","admin_krishna","proddatur","987654","admin"))
connection.commit()
connection.close()
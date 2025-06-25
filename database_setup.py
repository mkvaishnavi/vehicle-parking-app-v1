import sqlite3
connection=sqlite3.connect('database.db')
cursor=connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""CREATE TABLE User(
        User_ID INTEGER PRIMARY KEY,
        Username TEXT,
        Email TEXT,
        Password TEXT,
        Full_Name TEXT,
        Role TEXT
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

connection.commit()
connection.close()

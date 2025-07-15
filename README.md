# vehicle-parking-app-v1

## Author
Mudireddy Krishna Vaishnavi  
Roll No: 24F2009315  
Email: 24f2009315@ds.study.iitm.ac.in  

## Project Description
This is a web-based vehicle parking system that allows users to book and release parking spots across multiple parking lots. The application features separate dashboards for users and admins, role-based login/logout, and parking cost calculation based on time duration. It uses server-side rendering with no external APIs.

## Technologies Used
- Flask (Backend framework)
- Jinja2 (Templating engine)
- SQLite (Database using `sqlite3` module)
- HTML, CSS, Bootstrap (Frontend)
- Python `datetime` module

## How to Run the Project
1. Extract or clone the code folder.
2. Make sure Flask is installed:
pip install flask
3. Run the application:
python app.py
4. Open your browser and go to:
[http://127.0.0.1:5000/]

## Login Credentials
**Admin Login:**
- Email: admin@gmail.com  
- Password: admin123
**User Login:**
- You can register a new user from the signup page.

## Notes
- No REST API is implemented; the application uses server-side rendering via Flask and Jinja2.
- Bootstrap is included via CDN. No static folder is used.
- Foreign key constraints are enabled using:
PRAGMA foreign\_keys = ON;

## Video Link
https://drive.google.com/file/d/1Drl8UoDaTSSrHD_JAf7NEXCuNQHJBy6O/view?usp=sharing

## Folder Structure

VEHICLE_PARKING_APP_V1/
├── app.py  
├── database.db  
|── database_setup.py
|── test_database.py
├── templates/  
│   |── add_lot.html  
│   |── admin_dashboard.html  
│   |── all_parking_records.html  
│   |── edit_lot.html  
│   |── login.html  
|   |── register.html
|   |── user_dashboard.html
|   |── user_history.html
|   |── view_lot.html
|   |── view_spots.html
|   |── view_users.html
├── README.txt  

---

## AI/LLM Usage Summary
AI was used for around 30% of the project. Assistance was primarily taken for Flask integration patterns, session handling, and minor bug fixes. All HTML templates and Jinja2 logic were written manually by the author, and all business logic was implemented and tested independently.

## Status
✔️ Project completed and submitted as part of IITM MAD 1 milestone evaluation.
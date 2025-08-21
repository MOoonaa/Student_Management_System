# Student_Management_System
A Django-based web application to manage church students, attendance, and administration tasks.

##Features
-User authentication (register, login, logout)
-Admin dashboard
-Manage students
-Role-based access (admin vs students)
-Attendance tracking
-Student Profile (Name,Grade,Absence,CGPA)

##Installation and Set-up
###Clone the repo
git clone https://github.com/MOoonaa/Student_Management_System.git
###Navigate into the project folder
cd church_system_complete
###Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # On Windows
###Install dependencies
pip install -r requirements.txt
###Apply migrations
python manage.py migrate
###Create superuser
python manage.py createsuperuser
###Run the server
python manage.py runserver

##

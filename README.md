INEC Polling Unit & Aggregated Election Results Portal
A Django web application that displays election results at individual polling units, aggregates total votes across Local Government Areas (LGAs), and allows authorized users to submit new polling unit results into a MySQL database schema.

Features
Level 1: Individual Polling Unit Results: Search and view detailed party breakdown scores for any selected polling unit.

Level 2: LGA Aggregated Results: Select any Local Government Area (LGA) to calculate and display the total summed votes cast across all polling units in that LGA.

Level 3: Add Polling Unit Results: Form interface to record new polling units and enter election scores for all registered political parties simultaneously.

Prerequisites
Ensure you have the following installed on your machine:

Python 3.10+

MySQL Server (or MySQL Workbench / XAMPP)

Git

2. Set Up Virtual Environment
Bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows Command Prompt:
env\Scripts\activate

# On macOS/Linux:
source env/bin/activate

3. Install Dependencies
Bash
pip install django mysqlclient

Database Configuration
1. Create Database & Import SQL Dump
Open your MySQL terminal or MySQL Workbench and run:

SQL
CREATE DATABASE bincomphptest;

Import the provided bincom_test.sql file into the database:

Bash
# Using MySQL Command Line (Windows)
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p bincomphptest < path/to/bincom_test.sql

2. Configure Django Database Settings
Update bincom_project/settings.py with your MySQL credentials:

Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bincomphptest',
        'USER': 'root',
        'PASSWORD': 'MY_PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

1.Running the Application
Apply migrations:

Bash
python manage.py migrate

2.Start the development server:

Bash
python manage.py runserver

3.Open your browser and navigate to:

Plaintext
http://127.0.0.1:8000/

Navigation & Endpoints

Feature	URL Path	Description
Level 1	/	View results for individual polling units
Level 2	/lga-results/	View aggregated sum totals for LGAs
Level 3	/add-polling-unit/	Add a new polling unit and record party scores
Tech Stack
Backend: Python, Django 5.x

Database: MySQL

Frontend: HTML5, Bootstrap 5, Django Template Engine

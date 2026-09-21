# Student Grade Tracker

A desktop application built with **Python, Tkinter, and SQLite** for managing student records and grades.

## Features

* Add student records
* Add subjects and marks for each student
* Add new subjects dynamically
* View student information and grades
* Calculate individual student averages
* View class statistics
* Edit student information and grades
* Add subjects while editing a student
* Delete students and their associated grades
* Input validation for names, ages, and marks
* Persistent data storage using SQLite

## Technologies Used

* **Python**
* **Tkinter** - Graphical User Interface
* **SQLite** - Database storage

## Database Structure

The application uses two related tables:

### Students

Stores basic student information:

* Student ID
* Name
* Age

### Subjects

Stores the subjects and marks associated with each student:

* Subject ID
* Student ID
* Subject Name
* Mark

The `student_id` connects each student's records in the two tables.

## How to Run

### Requirements

* Python 3.x
* Tkinter (included with most standard Python installations)

### Run the Application

1. Download or clone this repository.

2. Open the project folder in **VS Code** or a terminal.

3. Run the following command:

```bash
dynamic.py
```

4. The application will open in a new window.

The SQLite database (`students.db`) is created automatically when the application is run for the first time.


## What I Learned

This project was developed to strengthen my practical programming and database skills. Through the project, I worked with:

* Python functions and control flow
* Tkinter GUI development
* SQLite databases
* SQL queries and CRUD operations
* Relationships between database tables
* Foreign keys
* Dynamic GUI elements
* Input validation
* Retrieving and updating database records

## Future Improvements

Potential future improvements include:

* Improved error message handling
* Student selection when multiple students have the same name
* Improved GUI styling
* Search and filtering options
* Grade reports and additional statistics

## Application Screenshots

### Main Dashboard

The main interface provides access to the application's student management and statistics features.

<img width="742" height="535" alt="Main Dashboard" src="https://github.com/user-attachments/assets/6d8be0ff-4f32-469f-8dbf-5537efe15087" />



### Add Student

Students can be added with their personal information, subject marks, and additional subjects as needed.

<img width="496" height="509" alt="Add Student" src="https://github.com/user-attachments/assets/8323f458-1196-4d87-9dcf-a7648dd9a647" />


### Student Records

Student records are retrieved from the SQLite database and displayed with their subjects, marks, and calculated individual averages.

<img width="623" height="727" alt="View Students" src="https://github.com/user-attachments/assets/fc5b2851-df12-42a7-980c-95de792e945a" />


### Class Statistics

Class-level statistics are calculated from the student grade data stored in the database.

<img width="498" height="290" alt="Class Statistics" src="https://github.com/user-attachments/assets/4f1c8c3e-e355-48ca-93a3-e38e17d4bb1b" />


## Author

**Jeziel Ramkaran**

BSc Electrical & Computer Engineering

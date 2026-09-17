import tkinter as tk
import sqlite3


# -----------------------------
# DATABASE SETUP
# -----------------------------

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

# Create students table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER
    )
""")

# Create subjects table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_name TEXT,
        mark REAL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
""")

connection.commit()
connection.close()


# -----------------------------
# MAIN WINDOW
# -----------------------------

window = tk.Tk()

window.title("Student Grade Tracker")
window.geometry("600x400")


title = tk.Label(
    window,
    text="Student Grade Tracker",
    font=("Arial", 20)
)

title.pack(pady=30)


# -----------------------------
# ADD STUDENT WINDOW
# -----------------------------

def add_student_window():

    student_window = tk.Toplevel(window)

    student_window.title("Add Student")
    student_window.geometry("400x700")


    # Student information
    tk.Label(
        student_window,
        text="Name"
    ).pack()

    name_entry = tk.Entry(student_window)
    name_entry.pack()


    tk.Label(
        student_window,
        text="Age"
    ).pack()

    age_entry = tk.Entry(student_window)
    age_entry.pack()


    # Standard subjects
    subjects = [
        "Math",
        "English",
        "Biology"
        
    ]


    # Store the Entry boxes
    mark_entries = {}


    # Create subject fields
    for subject in subjects:

        tk.Label(
            student_window,
            text=subject
        ).pack()

        mark_entry = tk.Entry(student_window)
        mark_entry.pack()

        mark_entries[subject] = mark_entry


    # -----------------------------
    # ADD SUBJECT
    # -----------------------------

    new_subject_entry = tk.Entry(student_window)

    def add_subject():

        new_subject = new_subject_entry.get()

        if new_subject == "":
            return

        subjects.append(new_subject)

        tk.Label(
            student_window,
            text=new_subject
        ).pack()

        mark_entry = tk.Entry(student_window)
        mark_entry.pack()

        mark_entries[new_subject] = mark_entry

        new_subject_entry.delete(0, tk.END)


    tk.Label(
        student_window,
        text="New Subject"
    ).pack(pady=(15, 0))

    new_subject_entry.pack()

    add_subject_button = tk.Button(
        student_window,
        text="+ Add Subject",
        command=add_subject
    )

    add_subject_button.pack(pady=5)


    # -----------------------------
    # SAVE STUDENT
    # -----------------------------

    def save_student():

        name = name_entry.get()
        age_text = age_entry.get()

        # Check name
        if name == "":
            tk.Label(
                student_window,
                text="Please enter a name."
            ).pack()

            return

        # Check age
        if age_text == "":
            tk.Label(
                student_window,
                text="Please enter an age."
            ).pack()

            return

        try:
            age = int(age_text)
        except ValueError:

            tk.Label(
                student_window,
                text="Age must be a number."
            ).pack()

            return

        # Check each subject mark
        for subject in subjects:

            mark_text = mark_entries[subject].get()

            if mark_text == "":
                tk.Label(
                    student_window,
                    text=f"Please enter a mark for {subject}."
                ).pack()

                return

            try:
                mark = float(mark_text)
            except ValueError:

                tk.Label(
                    student_window,
                    text=f"{subject} mark must be a number."
                ).pack()

                return

            if mark < 0 or mark > 100:

                tk.Label(
                    student_window,
                    text=f"{subject} mark must be between 0 and 100."
                ).pack()

                return

        # Save student
        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students (name, age)
            VALUES (?, ?)
        """, (name, age))

        student_id = cursor.lastrowid

        for subject in subjects:

            mark = float(mark_entries[subject].get())

            cursor.execute("""
                INSERT INTO subjects
                (student_id, subject_name, mark)
                VALUES (?, ?, ?)
            """, (student_id, subject, mark))

        connection.commit()
        connection.close()

        student_window.destroy()


    # Add Student button
    add_button = tk.Button(
        student_window,
        text="Add Student",
        command=save_student
    )

    add_button.pack(pady=20)

def view_students():

    view_window = tk.Toplevel(window)

    view_window.title("View Students")
    view_window.geometry("500x600")


    # Create a canvas for scrolling
    canvas = tk.Canvas(view_window)

    scrollbar = tk.Scrollbar(
        view_window,
        orient="vertical",
        command=canvas.yview
    )

    # Frame inside the canvas
    content_frame = tk.Frame(canvas)


    # Update the scroll region when the frame changes size
    content_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )


    # Put the frame inside the canvas
    canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
    )


    # Connect to database
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()


    # Get all students
    cursor.execute("""
        SELECT id, name, age
        FROM students
    """)

    students = cursor.fetchall()


    # Display each student
    for student in students:

        student_id = student[0]
        name = student[1]
        age = student[2]


        # Student name
        tk.Label(
            content_frame,
            text=f"Name: {name}",
            anchor="w"
        ).pack(
            fill="x",
            padx=20,
            pady=(10, 0)
        )


        # Student age
        tk.Label(
            content_frame,
            text=f"Age: {age}",
            anchor="w"
        ).pack(
            fill="x",
            padx=20
        )


        # Get subjects and marks
        cursor.execute("""
            SELECT subject_name, mark
            FROM subjects
            WHERE student_id = ?
        """, (student_id,))

        subjects = cursor.fetchall()


        # Display subjects
        for subject, mark in subjects:

            tk.Label(
                content_frame,
                text=f"{subject}: {mark}",
                anchor="w"
            ).pack(
                fill="x",
                padx=40
            )


        # Get average
        cursor.execute("""
            SELECT AVG(mark)
            FROM subjects
            WHERE student_id = ?
        """, (student_id,))

        average = cursor.fetchone()[0]


        # Display average
        if average is None:

            average_text = "Average: N/A"

        else:

            average_text = f"Average: {average:.2f}"


        tk.Label(
            content_frame,
            text=average_text,
            anchor="w"
        ).pack(
            fill="x",
            padx=20
        )


        # Separator
        tk.Label(
            content_frame,
            text="-" * 40,
            anchor="w"
        ).pack(
            fill="x",
            padx=20,
            pady=10
        )


    connection.close()


    # Put canvas and scrollbar into window
    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # Connect scrollbar to canvas
    canvas.configure(
        yscrollcommand=scrollbar.set
    )

def class_statistics():

    stats_window = tk.Toplevel(window)

    stats_window.title("Class Statistics")
    stats_window.geometry("400x400")


    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()


    # Get all students
    cursor.execute("""
        SELECT id, name
        FROM students
    """)

    students = cursor.fetchall()


    # Store student averages
    averages = []


    # Calculate each student's average
    for student in students:

        student_id = student[0]

        cursor.execute("""
            SELECT AVG(mark)
            FROM subjects
            WHERE student_id = ?
        """, (student_id,))

        average = cursor.fetchone()[0]


        # Only include students who have marks
        if average is not None:

            averages.append(average)


    connection.close()


    # Check if there are any averages
    if len(averages) == 0:

        tk.Label(
            stats_window,
            text="No student grades available."
        ).pack(pady=30)

        return


    # Calculate class statistics
    student_count = len(averages)

    class_average = sum(averages) / len(averages)

    highest_average = max(averages)

    lowest_average = min(averages)


    # Display statistics
    tk.Label(
        stats_window,
        text=f"Students with grades: {student_count}"
    ).pack(pady=10)


    tk.Label(
        stats_window,
        text=f"Class Average: {class_average:.2f}"
    ).pack(pady=10)


    tk.Label(
        stats_window,
        text=f"Highest Average: {highest_average:.2f}"
    ).pack(pady=10)


    tk.Label(
        stats_window,
        text=f"Lowest Average: {lowest_average:.2f}"
    ).pack(pady=10)



def edit_student():

    edit_window = tk.Toplevel(window)

    edit_window.title("Edit Student")
    edit_window.geometry("400x700")

    # -------------------------
    # Search for student
    # -------------------------

    tk.Label(
        edit_window,
        text="Search Student Name"
    ).pack()

    search_entry = tk.Entry(edit_window)
    search_entry.pack()

    # This frame will contain the student's information
    student_frame = tk.Frame(edit_window)
    student_frame.pack(fill="both", expand=True)

    def search_student():

        # Clear previous information
        for widget in student_frame.winfo_children():
            widget.destroy()

        search_name = search_entry.get()

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, age
            FROM students
            WHERE name = ?
        """, (search_name,))

        student = cursor.fetchone()

        if student is None:

            connection.close()

            tk.Label(
                student_frame,
                text="Student not found."
            ).pack(pady=20)

            return

        student_id = student[0]
        name = student[1]
        age = student[2]

        # -------------------------
        # Student information
        # -------------------------

        tk.Label(
            student_frame,
            text="Name"
        ).pack()

        name_entry = tk.Entry(student_frame)
        name_entry.pack()
        name_entry.insert(0, name)

        tk.Label(
            student_frame,
            text="Age"
        ).pack()

        age_entry = tk.Entry(student_frame)
        age_entry.pack()
        age_entry.insert(0, age)

        # -------------------------
        # Get student's subjects
        # -------------------------

        cursor.execute("""
            SELECT id, subject_name, mark
            FROM subjects
            WHERE student_id = ?
        """, (student_id,))

        subject_rows = cursor.fetchall()

        subject_entries = {}

        for subject_id, subject_name, mark in subject_rows:

            tk.Label(
                student_frame,
                text=subject_name
            ).pack()

            mark_entry = tk.Entry(student_frame)
            mark_entry.pack()

            mark_entry.insert(0, mark)

            subject_entries[subject_id] = mark_entry

        # -------------------------
        # Add Subject
        # -------------------------

        new_subject_entry = tk.Entry(student_frame)

        def add_subject():

            new_subject = new_subject_entry.get()

            if new_subject == "":
                return

            # Prevent duplicate subject names
            for subject_id in subject_entries:

                cursor.execute("""
                    SELECT subject_name
                    FROM subjects
                    WHERE id = ?
                """, (subject_id,))

                existing_subject = cursor.fetchone()

                if existing_subject and existing_subject[0] == new_subject:
                    return

            tk.Label(
                student_frame,
                text=new_subject
            ).pack()

            mark_entry = tk.Entry(student_frame)
            mark_entry.pack()

            # Use None to show that this is a new subject
            subject_entries[None] = (
                new_subject,
                mark_entry
            )

            new_subject_entry.delete(0, tk.END)

        tk.Label(
            student_frame,
            text="New Subject",
        ).pack(pady=(15, 0))

        new_subject_entry.pack()

        add_subject_button = tk.Button(
            student_frame,
            text="+ Add Subject",
            command=add_subject
        )
        add_subject_button.pack(pady=5)

        # -------------------------
        # Save Changes
        # -------------------------

        def save_changes():

            updated_name = name_entry.get()
            age_text = age_entry.get()

            # Check name
            if updated_name == "":
                tk.Label(
                    student_frame,
                    text="Please enter a name."
                ).pack()

                return

            # Check age
            if age_text == "":
                tk.Label(
                    student_frame,
                    text="Please enter an age."
                ).pack()

                return

            try:
                updated_age = int(age_text)
            except ValueError:

                tk.Label(
                    student_frame,
                    text="Age must be a number."
                ).pack()

                return

            # Check existing and new subjects
            for subject_id, entry in subject_entries.items():

                # Existing subject
                if subject_id is not None:

                    mark_text = entry.get()

                    if mark_text == "":
                        tk.Label(
                            student_frame,
                            text="Please enter a mark."
                        ).pack()

                        return

                    try:
                        mark = float(mark_text)
                    except ValueError:

                        tk.Label(
                            student_frame,
                            text="Mark must be a number."
                        ).pack()

                        return

                # New subject
                else:

                    subject_name = entry[0]
                    mark_entry = entry[1]

                    mark_text = mark_entry.get()

                    if mark_text == "":
                        tk.Label(
                            student_frame,
                            text=f"Please enter a mark for {subject_name}."
                        ).pack()

                        return

                    try:
                        mark = float(mark_text)
                    except ValueError:

                        tk.Label(
                            student_frame,
                            text=f"{subject_name} mark must be a number."
                        ).pack()

                        return

                # Check mark range
                if mark < 0 or mark > 100:

                    tk.Label(
                        student_frame,
                        text="Marks must be between 0 and 100."
                    ).pack()

                    return

            # -------------------------
            # Save changes
            # -------------------------

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE students
                SET name = ?, age = ?
                WHERE id = ?
            """, (
                updated_name,
                updated_age,
                student_id
            ))

            for subject_id, entry in subject_entries.items():

                # Existing subject
                if subject_id is not None:

                    mark = float(entry.get())

                    cursor.execute("""
                        UPDATE subjects
                        SET mark = ?
                        WHERE id = ?
                    """, (
                        mark,
                        subject_id
                    ))

                # New subject
                else:

                    subject_name = entry[0]
                    mark_entry = entry[1]

                    mark = float(mark_entry.get())

                    cursor.execute("""
                        INSERT INTO subjects
                        (student_id, subject_name, mark)
                        VALUES (?, ?, ?)
                    """, (
                        student_id,
                        subject_name,
                        mark
                    ))

            connection.commit()
            connection.close()

            edit_window.destroy()

            # -------------------------
# Save Changes button
# -------------------------

        save_button = tk.Button(
            student_frame,
            text="Save Changes",
            command=save_changes
    )

        save_button.pack(pady=20)

    

    search_button = tk.Button(
        edit_window,
        text="Search",
        command=search_student
    )
    search_button.pack(pady=10)

def delete_student():

    delete_window = tk.Toplevel(window)

    delete_window.title("Delete Student")
    delete_window.geometry("400x250")

    tk.Label(
        delete_window,
        text="Student Name"
    ).pack(pady=10)

    name_entry = tk.Entry(delete_window)
    name_entry.pack()

    def delete():

        name = name_entry.get()

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id
            FROM students
            WHERE name = ?
        """, (name,))

        student = cursor.fetchone()

        if student is None:

            tk.Label(
                delete_window,
                text="Student not found."
            ).pack(pady=10)

            connection.close()
            return

        student_id = student[0]

        # Delete the student's subjects
        cursor.execute("""
            DELETE FROM subjects
            WHERE student_id = ?
        """, (student_id,))

        # Delete the student
        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        connection.commit()
        connection.close()

        delete_window.destroy()

    delete_button = tk.Button(
        delete_window,
        text="Delete Student",
        command=delete
    )
    delete_button.pack(pady=20)





# -----------------------------
# MAIN BUTTON
# -----------------------------

add_button = tk.Button(
    window,
    text="Add Student",
    command=add_student_window
)

add_button.pack()

view_button = tk.Button(
    window,
    text="View Students",
    command=view_students
)

view_button.pack(pady=10)

stats_button = tk.Button(
    window,
    text="Class Statistics",
    command=class_statistics
)

stats_button.pack(pady=10)

edit_button = tk.Button( window, text="Edit Student", command=edit_student ) 
edit_button.pack(pady=10)

delete_button = tk.Button(
    window,
    text="Delete Student",
    command=delete_student
)

delete_button.pack(pady=10)


# -----------------------------
# START PROGRAM
# -----------------------------

window.mainloop()
# Student-Result-Management
This project is a Python Tkinter desktop application integrated with MySQL for managing student records. It combines a clean graphical interface with robust database operations, offering a complete solution for academic record management, performance visualization, and peer communication.

✨ Key Features
Add Student: Insert new records with ID, name, roll number, class, and subject marks.
Update Student: Modify existing student details and scores.
Delete Student: Remove records by student ID.
View Students: Display all records in a tabular format with calculated averages.
Performance Graph: Visualize subject-wise marks using Matplotlib bar charts.
Student Chat System: Real-time messaging between students with timestamps stored in the database.

🛠️ Tech Stack
Python: Tkinter, ttk, ScrolledText, Matplotlib
MySQL Connector: Database integration
MySQL Database: Tables for students and messages
Datetime: Timestamp management

📊 Database Schema
students: student_id, name, roll_no, class, physics, chemistry, maths, english
messages: sender_id, receiver_id, message, msg_time

🚀 How to Run
1.Install dependencies:
      pip install mysql-connector-python matplotlib
2.Create a MySQL database named school with students and messages tables.
3.Run the script:
      python student_management.py
      
🎯 Purpose
This system is designed for schools, training centers, and academic projects to manage student records efficiently. It demonstrates GUI design, CRUD operations, database integration, and data visualization in Python, making it a strong portfolio project for developers exploring full‑stack desktop applications.

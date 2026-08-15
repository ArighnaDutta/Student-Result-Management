from tkinter import *
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="school",
    port=3306,
    charset="utf8"
)

cur = con.cursor()

root = Tk()
root.title("Advanced Student Management System")
root.geometry("1000x750")
root.configure(bg="lightblue")

def clear_fields():

    e_id.delete(0, END)
    e_name.delete(0, END)
    e_roll.delete(0, END)
    e_class.delete(0, END)
    e_phy.delete(0, END)
    e_chem.delete(0, END)
    e_math.delete(0, END)
    e_eng.delete(0, END)

def add_student():

    try:

        query = """
        INSERT INTO students
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            int(e_id.get()),
            e_name.get(),
            int(e_roll.get()),
            e_class.get(),
            float(e_phy.get()),
            float(e_chem.get()),
            float(e_math.get()),
            float(e_eng.get())
        )

        cur.execute(query, values)
        con.commit()

        messagebox.showinfo(
            "Success",
            "Student Added Successfully"
        )

        clear_fields()

    except:

        messagebox.showerror(
            "Error",
            "Student ID Already Exists"
        )

def update_student():

    query = """
    UPDATE students
    SET name=%s,
        roll_no=%s,
        class=%s,
        physics=%s,
        chemistry=%s,
        maths=%s,
        english=%s
    WHERE student_id=%s
    """

    values = (
        e_name.get(),
        int(e_roll.get()),
        e_class.get(),
        float(e_phy.get()),
        float(e_chem.get()),
        float(e_math.get()),
        float(e_eng.get()),
        int(e_id.get())
    )

    cur.execute(query, values)
    con.commit()

    if cur.rowcount > 0:

        messagebox.showinfo(
            "Success",
            "Record Updated Successfully"
        )

        clear_fields()

    else:

        messagebox.showerror(
            "Error",
            "Student ID Not Found"
        )

def delete_student():

    sid = e_id.get()

    query = "DELETE FROM students WHERE student_id=%s"

    cur.execute(query, (sid,))
    con.commit()

    if cur.rowcount > 0:

        messagebox.showinfo(
            "Success",
            "Student Record Deleted"
        )

        clear_fields()

    else:

        messagebox.showerror(
            "Error",
            "Student ID Not Found"
        )

def view_students():

    top = Toplevel()
    top.title("Student Records")
    top.geometry("1200x400")

    tree = ttk.Treeview(top)

    tree["columns"] = (
        "ID",
        "Name",
        "Roll",
        "Class",
        "Physics",
        "Chemistry",
        "Maths",
        "English",
        "Average"
    )

    tree.column("#0", width=0, stretch=NO)

    tree.column("ID", width=100, anchor=CENTER)
    tree.column("Name", width=180, anchor=CENTER)
    tree.column("Roll", width=100, anchor=CENTER)
    tree.column("Class", width=100, anchor=CENTER)
    tree.column("Physics", width=100, anchor=CENTER)
    tree.column("Chemistry", width=100, anchor=CENTER)
    tree.column("Maths", width=100, anchor=CENTER)
    tree.column("English", width=100, anchor=CENTER)
    tree.column("Average", width=100, anchor=CENTER)

    tree.heading("#0", text="")

    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Roll", text="Roll No")
    tree.heading("Class", text="Class")
    tree.heading("Physics", text="Physics")
    tree.heading("Chemistry", text="Chemistry")
    tree.heading("Maths", text="Maths")
    tree.heading("English", text="English")
    tree.heading("Average", text="Average")

    cur.execute("SELECT * FROM students")

    records = cur.fetchall()

    count = 0

    for row in records:

        avg = (
            row[4] +
            row[5] +
            row[6] +
            row[7]
        ) / 4

        tree.insert(
            parent="",
            index="end",
            iid=count,
            values=(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                round(avg,2)
            )
        )

        count += 1

    tree.pack(fill=BOTH, expand=True)

def show_graph():

    sid = int(e_id.get())

    query = """
    SELECT physics, chemistry, maths, english
    FROM students
    WHERE student_id=%s
    """

    cur.execute(query, (sid,))

    data = cur.fetchone()

    if data:

        subjects = [
            "Physics",
            "Chemistry",
            "Maths",
            "English"
        ]

        marks = [
            data[0],
            data[1],
            data[2],
            data[3]
        ]

        plt.figure(figsize=(7,5))

        plt.bar(subjects, marks)

        plt.xlabel("Subjects")
        plt.ylabel("Marks")
        plt.title("Student Performance")

        plt.ylim(0,100)

        plt.show()

    else:

        messagebox.showerror(
            "Error",
            "Student ID Not Found"
        )

def open_chat():

    sender = int(chat_sender.get())
    receiver = int(chat_receiver.get())

    cur.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (sender,)
    )

    if not cur.fetchone():

        messagebox.showerror(
            "Error",
            "Sender ID Not Found"
        )

        return

    cur.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (receiver,)
    )

    if not cur.fetchone():

        messagebox.showerror(
            "Error",
            "Receiver ID Not Found"
        )

        return

    chat_win = Toplevel()
    chat_win.title("Student Chatbox")
    chat_win.geometry("600x500")

    Label(
        chat_win,
        text=f"Chat : {sender} → {receiver}",
        font=("Arial", 14, "bold")
    ).pack(pady=5)

    chat_area = ScrolledText(
        chat_win,
        width=70,
        height=20,
        font=("Arial", 11)
    )

    chat_area.pack(pady=10)

    query = """
    SELECT sender_id, message, msg_time
    FROM messages
    WHERE
    (sender_id=%s AND receiver_id=%s)
    OR
    (sender_id=%s AND receiver_id=%s)
    ORDER BY msg_time
    """

    values = (
        sender,
        receiver,
        receiver,
        sender
    )

    cur.execute(query, values)

    chats = cur.fetchall()

    for msg in chats:

        line = (
            f"Student {msg[0]} : "
            f"{msg[1]} "
            f"({msg[2]})\n"
        )

        chat_area.insert(END, line)

    msg_entry = Entry(
        chat_win,
        width=45,
        font=("Arial", 12)
    )

    msg_entry.pack(side=LEFT, padx=10, pady=10)

    def send_message():

        msg = msg_entry.get()

        if msg.strip() == "":
            return

        query = """
        INSERT INTO messages
        (sender_id, receiver_id, message, msg_time)
        VALUES (%s,%s,%s,%s)
        """

        values = (
            sender,
            receiver,
            msg,
            datetime.now()
        )

        cur.execute(query, values)
        con.commit()

        line = (
            f"Student {sender} : "
            f"{msg} "
            f"({datetime.now().strftime('%H:%M:%S')})\n"
        )

        chat_area.insert(END, line)

        msg_entry.delete(0, END)

    Button(
        chat_win,
        text="Send",
        bg="lightgreen",
        command=send_message
    ).pack(side=LEFT, padx=5)

Label(
    root,
    text="ADVANCED STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="lightblue"
).pack(pady=10)

frame = Frame(root, bg="lightblue")
frame.pack(pady=10)

Label(frame, text="Student ID", bg="lightblue").grid(row=0,column=0,padx=10,pady=5)
e_id = Entry(frame)
e_id.grid(row=0,column=1)

Label(frame, text="Name", bg="lightblue").grid(row=1,column=0,padx=10,pady=5)
e_name = Entry(frame)
e_name.grid(row=1,column=1)

Label(frame, text="Roll No", bg="lightblue").grid(row=2,column=0,padx=10,pady=5)
e_roll = Entry(frame)
e_roll.grid(row=2,column=1)

Label(frame, text="Class", bg="lightblue").grid(row=3,column=0,padx=10,pady=5)
e_class = Entry(frame)
e_class.grid(row=3,column=1)

Label(frame, text="Physics", bg="lightblue").grid(row=4,column=0,padx=10,pady=5)
e_phy = Entry(frame)
e_phy.grid(row=4,column=1)

Label(frame, text="Chemistry", bg="lightblue").grid(row=5,column=0,padx=10,pady=5)
e_chem = Entry(frame)
e_chem.grid(row=5,column=1)

Label(frame, text="Maths", bg="lightblue").grid(row=6,column=0,padx=10,pady=5)
e_math = Entry(frame)
e_math.grid(row=6,column=1)

Label(frame, text="English", bg="lightblue").grid(row=7,column=0,padx=10,pady=5)
e_eng = Entry(frame)
e_eng.grid(row=7,column=1)

btn_frame = Frame(root, bg="lightblue")
btn_frame.pack(pady=20)

Button(
    btn_frame,
    text="Add Student",
    width=15,
    bg="lightgreen",
    command=add_student
).grid(row=0,column=0,padx=10)

Button(
    btn_frame,
    text="Update Student",
    width=15,
    bg="lightyellow",
    command=update_student
).grid(row=0,column=1,padx=10)

Button(
    btn_frame,
    text="Delete Student",
    width=15,
    bg="red",
    fg="white",
    command=delete_student
).grid(row=0,column=2,padx=10)

Button(
    btn_frame,
    text="View Students",
    width=15,
    bg="orange",
    command=view_students
).grid(row=0,column=3,padx=10)

Button(
    btn_frame,
    text="Show Graph",
    width=15,
    bg="pink",
    command=show_graph
).grid(row=0,column=4,padx=10)

chat_frame = LabelFrame(
    root,
    text="Student Chat System",
    padx=20,
    pady=20,
    bg="lightblue",
    font=("Arial",12,"bold")
)

chat_frame.pack(pady=20)

Label(
    chat_frame,
    text="Sender ID",
    bg="lightblue"
).grid(row=0,column=0,padx=10)

chat_sender = Entry(chat_frame)
chat_sender.grid(row=0,column=1,padx=10)

Label(
    chat_frame,
    text="Receiver ID",
    bg="lightblue"
).grid(row=0,column=2,padx=10)

chat_receiver = Entry(chat_frame)
chat_receiver.grid(row=0,column=3,padx=10)

Button(
    chat_frame,
    text="Open Chat",
    bg="lightgreen",
    command=open_chat
).grid(row=0,column=4,padx=10)

Button(
    root,
    text="Exit",
    width=20,
    bg="black",
    fg="white",
    command=root.destroy
).pack(pady=20)

root.mainloop()

con.close() 

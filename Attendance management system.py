from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# ---------------- FUNCTIONS ---------------- #

def add_attendance():
    roll = roll_entry.get()
    name = name_entry.get()
    status = status_var.get()

    if roll == "" or name == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    tree.insert("", END, values=(roll, name, status, date))

    update_summary()

    roll_entry.delete(0, END)
    name_entry.delete(0, END)

def delete_record():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a record first")
        return

    tree.delete(selected)
    update_summary()

def search_student():
    search = search_entry.get().lower()

    for item in tree.get_children():
        values = tree.item(item)["values"]

        if search in str(values[0]).lower() or search in str(values[1]).lower():
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
            return

    messagebox.showinfo("Search", "Student not found")

def save_attendance():
    with open("attendance_records.txt", "w") as file:
        for row in tree.get_children():
            values = tree.item(row)["values"]
            file.write(",".join(map(str, values)) + "\n")

    messagebox.showinfo("Success", "Attendance saved successfully!")

def update_summary():
    total = len(tree.get_children())

    present = 0
    absent = 0

    for row in tree.get_children():
        status = tree.item(row)["values"][2]

        if status == "Present":
            present += 1
        else:
            absent += 1

    total_label.config(text=f"Total Students: {total}")
    present_label.config(text=f"Present: {present}")
    absent_label.config(text=f"Absent: {absent}")

# ---------------- GUI ---------------- #

root = Tk()
root.title("Attendance Management System")
root.geometry("1000x600")

title = Label(
    root,
    text="Attendance Management System",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

author = Label(
    root,
    text="Developed By: Narendra Meda",
    font=("Arial", 10, "italic")
)
author.pack()

# Input Frame
frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Roll No").grid(row=0, column=0, padx=5)

roll_entry = Entry(frame)
roll_entry.grid(row=0, column=1)

Label(frame, text="Name").grid(row=0, column=2, padx=5)

name_entry = Entry(frame)
name_entry.grid(row=0, column=3)

status_var = StringVar()
status_var.set("Present")

OptionMenu(frame, status_var, "Present", "Absent").grid(row=0, column=4)

Button(
    frame,
    text="Add Attendance",
    command=add_attendance
).grid(row=0, column=5, padx=10)

# Search
search_frame = Frame(root)
search_frame.pack(pady=10)

Label(search_frame, text="Search").grid(row=0, column=0)

search_entry = Entry(search_frame, width=30)
search_entry.grid(row=0, column=1)

Button(
    search_frame,
    text="Search Student",
    command=search_student
).grid(row=0, column=2, padx=10)

# Table
columns = ("Roll No", "Name", "Status", "Date & Time")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=220)

tree.pack(pady=20)

# Buttons
button_frame = Frame(root)
button_frame.pack()

Button(
    button_frame,
    text="Delete Selected",
    bg="red",
    fg="white",
    command=delete_record
).grid(row=0, column=0, padx=10)

Button(
    button_frame,
    text="Save Attendance",
    bg="green",
    fg="white",
    command=save_attendance
).grid(row=0, column=1, padx=10)

# Dashboard
dashboard = Frame(root)
dashboard.pack(pady=20)

total_label = Label(
    dashboard,
    text="Total Students: 0",
    font=("Arial", 12, "bold")
)
total_label.grid(row=0, column=0, padx=20)

present_label = Label(
    dashboard,
    text="Present: 0",
    font=("Arial", 12, "bold")
)
present_label.grid(row=0, column=1, padx=20)

absent_label = Label(
    dashboard,
    text="Absent: 0",
    font=("Arial", 12, "bold")
)
absent_label.grid(row=0, column=2, padx=20)

root.mainloop()
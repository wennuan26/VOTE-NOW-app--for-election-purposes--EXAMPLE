from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# from PIL import Image
import sqlite3
import os

def open_page(page_script):
    root.destroy()
    os.system(f'python {page_script}')

# Function for login action
def login_action():
    email = email_entry.get()
    password = password_entry.get()
    role = role_var.get()

    try:
        with sqlite3.connect('vo_system.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=? AND role=?", (email, password, role))
            user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", f"Welcome {user[1]}!")
            if role == "Voter":
                try:
                    root.destroy()
                    import voter_dash
                    voter_dash.voter_dashboard(user[0])  # Pass user_id
                except ImportError:
                    messagebox.showerror("Error", "Voter dashboard module not found!")
            elif role == "Candidate":
                try:
                    root.destroy()
                    import candidate_dash
                    candidate_dash.candidate_dashboard(user[0])  # Pass user_id
                except ImportError:
                    messagebox.showerror("Error", "Candidate dashboard module not found!")
            elif role == "Admin":
                try:
                    root.destroy()
                    import admin_panel
                    admin_panel.admin(user[0])  # Open admin panel
                except ImportError:
                    messagebox.showerror("Error", "Admin panel module not found!")
            else:
                messagebox.showerror("Error", "Invalid role selected!")
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Login GUI
root = Tk()
root.title("Login")
root.geometry("400x300")
root.configure(bg='#6495ED')
root.resizable(width=False, height=False)

# Apply styles
style = ttk.Style()
style.theme_use("clam")

# Button style
style.configure("SoftRound.TButton",
                background="#483D8B",
                foreground="white",
                font=("Ubuntu Mono", 12,"bold"),
                padding=6,
                borderwidth=2,
                relief="flat")
style.map("SoftRound.TButton",
          background=[("active", "#005a9e")])

# Label style
style.configure("Label.TLabel",
                font=("Ubuntu Mono", 12, "bold"),
                background="#6495ED",
                foreground="#483D8B",
                padding=5)

# Combobox style
style.configure("TCombobox",
                fieldbackground="#f9f9f9",
                background="#007acc",
                foreground="#333333",
                font=("Ubuntu Mono", 12))

ttk.Label(root, text="Email 📩 :", style="Label.TLabel").pack(pady=10)
email_entry = ttk.Entry(root, width=30, font=("Ubuntu Mono", 12))
email_entry.pack()

ttk.Label(root, text="Password 🔑 :", style="Label.TLabel").pack(pady=10)
password_entry = ttk.Entry(root, width=30, font=("Ubuntu Mono", 12), show="*")
password_entry.pack()

role_var = StringVar(value="Voter")
roles = ["Voter", "Candidate", "Admin"]
combobox = ttk.Combobox(root, textvariable=role_var, values=roles, style="TCombobox", state="readonly")
combobox.pack(pady=10)

# Login and Back buttons
ttk.Button(root, text="Login 👤", style="SoftRound.TButton", command=login_action).pack(pady=3)
ttk.Button(root, text="Back 🔙", style="SoftRound.TButton", command=lambda: open_page('main_app.py')).pack(pady=3)

root.mainloop()

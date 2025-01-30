from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import os
from PIL import Image,ImageTk
def open_page(page_script):
    root.destroy()
    os.system(f'python {page_script}')

def signup_action():
    name = name_entry.get()
    nic = nic_entry.get()
    email = email_entry.get()
    pwd = password_entry.get()
    role = role_var.get()
    district = district_var.get()

    if not name or not nic or not email or not pwd or not district:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect('vo_system.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, nic, email, password, role, district) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, nic, email, pwd, role, district))
        conn.commit()
        messagebox.showinfo("Success", "Signup successful!")
        root.destroy()
        import login_page
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "NIC or email already exists.")
    finally:
        conn.close()

# Initialize the root window
root = Tk()
root.title("Sign Up")
root.geometry("950x500")
root.resizable(False, False)
root.configure(background='#6495ED')

# Configure styles
style = ttk.Style()
style.theme_use("clam")

# General frame style
style.configure("TFrame", background="#6495ED", relief="flat")

# Header Label style
style.configure("Header.TLabel", font=("Ubuntu Mono", 25, "bold"), foreground="#333333", background="#6495ED", padding=10)

# Label style for input fields
style.configure("Input.TLabel", font=("Ubuntu Mono", 12,'bold'), foreground="#333333", background="#6495ED", padding=5)

# Combobox style
style.configure("TCombobox",background="#007acc",fieldbackground="#f9f9f9",foreground="#333333", font=("Ubuntu Mono", 12))

# Soft round button style
style.configure(
    "SoftRound.TButton",
    background="#483D8B",
    foreground="white",
    font=("Ubuntu Mono", 12),
    padding=10,
    borderwidth=2,
    relief="flat",
    anchor="center"
)
style.map(
    "SoftRound.TButton",
    background=[("active", "#005a9e")],
    bordercolor=[("active", "#005a9e"), ("!active", "#007acc")],
    relief=[("pressed", "sunken"), ("!pressed", "flat")]
)

# Create a frame for the content
frame = ttk.Frame(root, style="TFrame", padding="20")
frame.pack(expand=True, fill=BOTH)

# Title Label
ttk.Label(frame, text="Sign Up", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

# Load the image
image_path = r"F:\V System\vote1.jpg"  # Use raw string literal to handle backslashes
image = Image.open(image_path)
image = image.resize((400,400), Image.Resampling.LANCZOS)  # Use the correct resampling method
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(frame, image=photo, background="#6495ED")
image_label.image = photo  # Keep a reference to avoid garbage collection
image_label.grid(row=0, column=2, rowspan=9, padx=110, pady=20, sticky="ne")

# Name
ttk.Label(frame, text="Name:", style="Input.TLabel").grid(row=1, column=0, pady=5, sticky="e")
name_entry = ttk.Entry(frame,width=30, font=("Ubuntu Mono", 12))
name_entry.grid(row=1, column=1, pady=5)

# NIC
ttk.Label(frame, text="NIC:", style="Input.TLabel").grid(row=2, column=0, pady=5, sticky="e")
nic_entry = ttk.Entry(frame,width=30, font=("Ubuntu Mono", 12))
nic_entry.grid(row=2, column=1, pady=5)

# Email
ttk.Label(frame, text="Email:", style="Input.TLabel").grid(row=3, column=0, pady=5, sticky="e")
email_entry = ttk.Entry(frame, width=30, font=("Ubuntu Mono", 12))
email_entry.grid(row=3, column=1, pady=5)

# Password
ttk.Label(frame, text="Password:", style="Input.TLabel").grid(row=4, column=0, pady=5, sticky="e")
password_entry = ttk.Entry(frame, width=30, font=("Ubuntu Mono", 12), show="*")
password_entry.grid(row=4, column=1, pady=5)

# Role
ttk.Label(frame, text="Role:", style="Input.TLabel").grid(row=5, column=0, pady=5, sticky="e")
role_var = StringVar(value="Voter")
roles = ["Voter", "Candidate"]
role_combobox = ttk.Combobox(frame, textvariable=role_var, values=roles, state="readonly", width=28, style="TCombobox")
role_combobox.grid(row=5, column=1, pady=5)

# District
ttk.Label(frame, text="District:", style="Input.TLabel").grid(row=6, column=0, pady=5, sticky="e")
district_var = StringVar()
districts = [
    "Ampara",
    "Anuradhapura",
    "Badulla",
    "Batticaloa",
    "Colombo",
    "Galle",
    "Gampaha",
    "Hambantota",
    "Jaffna",
    "Kalutara",
    "Kandy",
    "Kegalle",
    "Kilinochchi",
    "Kurunegala",
    "Mannar",
    "Matale",
    "Matara",
    "Monaragala",
    "Mullaitivu",
    "Nuwara Eliya",
    "Polonnaruwa",
    "Puttalam",
    "Ratnapura",
    "Trincomalee",
    "Vavuniya",
]
district_combobox = ttk.Combobox(frame, textvariable=district_var, values=districts, state="readonly", width=28, style="TCombobox")
district_combobox.grid(row=6, column=1, pady=5)

# Sign Up Button
signup_button = ttk.Button(frame, text="Sign Up", style="SoftRound.TButton", command=signup_action)
signup_button.grid(row=7, column=1, pady=20, sticky="e")
ttk.Button(frame, text="Back", command=lambda: open_page('main_app.py'),style='SoftRound.TButton').grid(row=8, column=1, pady=1, sticky="e")
# Start the main loop
root.mainloop()

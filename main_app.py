from tkinter import *
import os
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize the root window first
root = Tk()
root.title('Election Voting System - Sri Lanka - Welcome Page')
root.geometry('950x500')
root.resizable(False, False)
root.configure(background="#6495ED")

# Create a frame for the content
frame = ttk.Frame(root, padding="20", style="TFrame")
frame.pack(expand=True, fill=BOTH)

def open_page(page_script):
    root.destroy()
    os.system(f'python {page_script}')

# Load the image
image_path = r"F:\V System\vote1.jpg"  # Use raw string literal to handle backslashes
image = Image.open(image_path)
image = image.resize((400,400), Image.Resampling.LANCZOS)  # Use the correct resampling method
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(frame, image=photo, background="#6495ED")
image_label.image = photo  # Keep a reference to avoid garbage collection
image_label.grid(row=0, column=2, rowspan=6, padx=20, pady=20, sticky="ne")

# Configure styles
style = ttk.Style()
style.theme_use("clam")

# General styles for frame and header
style.configure("Header.TLabel", font=("Ubuntu Mono", 20, "bold"), foreground="#333333", background="#6495ED", padding=20)
style.configure("TFrame", background="#6495ED")

# Soft round button style
style.configure(
    "SoftRound.TButton",
    background="#483D8B",
    foreground="white",
    font=("Ubuntu Mono", 12),
    padding=10,
    width=15,
    borderwidth=2,
    relief="flat",
    anchor="center",
)
style.map(
    "SoftRound.TButton",
    background=[("active", "#005a9e")],
    bordercolor=[("active", "#005a9e"), ("!active", "#007acc")],
    relief=[("pressed", "sunken"), ("!pressed", "flat")],
)

# Title Label
ttk.Label(frame, text="Welcome to the Voting System", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

# Exit Application Function
def exit_app():
    root.destroy()

# Buttons with soft round styles
ttk.Button(frame, text="Login 👤 ", command=lambda: open_page('login_page.py'), style="SoftRound.TButton").grid(row=1, column=0, pady=10)
ttk.Button(frame, text="Sign Up 👥 ", command=lambda: open_page('signup_page.py'), style="SoftRound.TButton").grid(row=2, column=0, pady=10)
ttk.Button(frame, text="Vote Now ❎ ", command=lambda: open_page('login_page.py'), style="SoftRound.TButton").grid(row=3, column=0, pady=10)
ttk.Button(frame, text="User Guide 🔍", command=lambda: open_page('about.py'), style="SoftRound.TButton").grid(row=4, column=0, pady=10)
ttk.Button(frame, text="Exit ", command=exit_app, style="SoftRound.TButton").grid(row=5, column=0, pady=10)

# Adjust window size dynamically based on content
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Start the main loop
root.mainloop()

from tkinter import *
import os
from tkinter import ttk

def open_page(page_script):
    root.destroy()  # Close the current window
    os.system(f'python {page_script}')  # Open the main app script

# Initialize the root window
root = Tk()
root.title('Election Voting System - Sri Lanka - About')
root.geometry('950x500')
root.resizable(False, False)
root.configure(background='#6495ED')

# Configure styles
style = ttk.Style()
style.theme_use("clam")

# General styles for frame and header
style.configure("Header.TLabel", font=("Ubuntu Mono", 20, "bold"), foreground="#483D8B", background="#6495ED", padding=20)
style.configure("TFrame", background="#6495ED")

# Soft round button style
style.configure(
    "SoftRound.TButton",
    background="#483D8B",
    foreground="white",
    font=("Ubuntu Mono", 12),
    padding=10,
    borderwidth=2,
    relief="flat",
    anchor="center",
)
style.map(
    "SoftRound.TButton",
    background=[("active", "#005a9e")],
    bordercolor=[("active", "#005a9e"), ("!active", "#483D8B")],
    relief=[("pressed", "sunken"), ("!pressed", "flat")],
)

# Create a frame for the content
frame = ttk.Frame(root, padding="20", style="TFrame")
frame.grid(row=0, column=0, sticky="nsew")

# Title Label
ttk.Label(frame, text="About & Guidelines", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

# Text content with wrapping
content_text = """

                            WELCOME TO VOTE Now ✔️ SRI LANKA APP

● VOTE Now is a comprehensive and user-friendly dashboard 😊
    designed to facilitate the efficient management of the voting process. 🛠️

● Built with Python’s Tkinter framework and backed by an SQLite database, 
    It provides an all-in-one solution for administrators to oversee 
                                                            voter registration,
                                                            candidate management, 
                                                            real-time election results.
 
● VOTE Now empowers admins with an intuitive interface and 
    essential tools to streamline electoral tasks and 
    ensure a smooth voting experience for all participants.

Key Features:

1. User Management: 
            Effortlessly add, edit voter accounts with a secure database.
    
2. Candidate Management: 
            Manage candidate profiles, 
            Deleting outdated entries.
            
3. Real-Time Results: 
            Access live voting results with clear and concise data visualization.
            
4. Polished UI: Styled widgets and a responsive layout for a professional and intuitive user experience.

-------------------------------------------------------------------------

User Guidelines

1. Accessing the Dashboard:

- Ensure the application is installed on your system.
- Open the VOTE Now - main app.py application and log in with the admin credentials.

2. Managing Users:

- Navigate to the “User Management” section.
- Use the “Add Candidate” button to register a new candidate for election Process.
- Select a Candidate from the list and click “Delete” to remove them.
- Ensure accurate information is entered to prevent duplicates or errors.
- Select and delete candidates who are no longer eligible or valid for the election.

4. Viewing Results:

- Navigate to the “Results” tab.
- Review live updates of the election results in an easy-to-understand format.
- Export results if needed for record-keeping or publication.

5. Security Measures:

- Ensure only authorized personnel have access to the admin dashboard.
- Regularly update passwords and avoid sharing credentials.

6. Troubleshooting Tips:

- If the application encounters errors, restart it and verify the database connection.
- Check for updates to ensure you’re using the latest version.
- Contact technical support if issues persist.

TECHNICAL DETAILS
------- name               :chei-MinerYa
------- e-mail              :zhaomingli26@gmail.com / thathsandi.uog06@edu.lnbti.lk
------- phone number  :+947 767 642 644
------- github              :chei

7. Best Practices:

- Double-check all entries for accuracy before saving.
- Maintain a clean and organized database by removing inactive users and candidates.
- Monitor results periodically to detect any anomalies early.

By following these guidelines, administrators can maximize the efficiency and reliability of the Voter Dash application, ensuring a seamless experience for all stakeholders involved in the voting process."""

# Create canvas and scrollbar
canvas = Canvas(frame, bg="#6495ED", height=300,width=900)
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
scrollable_frame = Frame(canvas, bg="#6495ED")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add the content text to the scrollable frame
content_label = Label(scrollable_frame, text=content_text, font=("Ubuntu Mono", 15), fg="#483D8B", bg="#6495ED", justify=LEFT, wraplength=900)
content_label.grid(padx=20, pady=10)

# Configure grid for canvas and scrollbar
canvas.grid(row=1, column=0, sticky="nsew")
scrollbar.grid(row=1, column=1, sticky="ns")

# Back button
ttk.Button(frame, text="Back", command=lambda: open_page('main_app.py'), style="SoftRound.TButton").grid(row=2, column=0, pady=10)

# Adjust window size dynamically based on content
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Update canvas scroll region after widgets are placed
scrollable_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Start the main loop
root.mainloop()

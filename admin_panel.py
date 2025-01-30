import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from candidate_dash import candidate_dashboard  # Ensure this module exists and is correctly implemented

def admin():
    def open_page(page_script):
        root.destroy()
        os.system(f'python {page_script}')
    # Main Admin Panel Window
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry('950x500')
    root.resizable(width=False, height=False)
    root.configure(bg='#6495ED')

    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")

    # General style
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
        bordercolor=[("active", "#005a9e"), ("!active", "#483D8B")],
        relief=[("pressed", "sunken"), ("!pressed", "flat")],
    )
    style.configure(
        "Header.TLabel",
        font=("Ubuntu Mono", 20, "bold"),
        background="#6495ED",
        foreground="#483D8B",
        padding=5
    )
    style.configure(
        "Label.TLabel",
        font=("Ubuntu Mono", 12, "bold"),
        background="#6495ED",
        foreground="#483D8B",
        padding=5
    )
    style.configure(
        "Treeview",
        font=("Ubuntu Mono", 12),
        foreground="#333333",
        rowheight=25
    )
    style.configure(
        "Treeview.Heading",
        font=("Ubuntu Mono", 12, "bold"),
        background="#333333",
        foreground="#f9f9f9",
    )
    style.configure(
        style="TFrame",
        background="#6495ED",
    )

    frame = ttk.Frame(root, padding="20", style="TFrame")
    frame.pack(expand=True, fill=tk.BOTH)

    # Header
    ttk.Label(frame, text="Welcome to the Admin Dash Board", style="Header.TLabel").grid(row=0, column=0, columnspan=2,
                                                                                         pady=20)

    # View Users Function
    def view_users():
        def display_users(search_query=""):
            with sqlite3.connect('vo_system.db') as conn:
                cursor = conn.cursor()
                # Fetch distinct roles
                cursor.execute("SELECT DISTINCT role FROM users")
                roles = [role[0] for role in cursor.fetchall()]

                # Clear existing tabs
                for tab in notebook.tabs():
                    notebook.forget(tab)

                for role in roles:
                    # Fetch users based on role and search query
                    query = f"%{search_query}%"
                    cursor.execute(
                        "SELECT id, name, email, role, password,district FROM users WHERE role=? AND (name LIKE ? OR email LIKE ?)",
                        (role, query, query),
                    )
                    users = cursor.fetchall()

                    # Create a new frame for the role
                    role_frame = ttk.Frame(notebook)
                    notebook.add(role_frame, text=role)

                    # Treeview for displaying users
                    columns = ("ID", "Name", "Email", "Role", "Password","District")
                    tree = ttk.Treeview(role_frame, columns=columns, show="headings", style="Treeview")
                    for col in columns:
                        tree.heading(col, text=col, anchor=tk.CENTER)
                        tree.column(col, width=150, anchor=tk.CENTER)

                    for i, user in enumerate(users):
                        tag = "evenrow" if i % 2 == 0 else "oddrow"
                        tree.insert("", tk.END, values=user, tags=(tag,))
                    tree.tag_configure("evenrow", background="#e6f7ff")
                    tree.tag_configure("oddrow", background="#ffffff")

                    # Add Treeview and scrollbar to frame
                    tree.pack(pady=10, fill=tk.BOTH, expand=True)
                    scrollbar = ttk.Scrollbar(role_frame, orient=tk.VERTICAL, command=tree.yview)
                    tree.configure(yscroll=scrollbar.set)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def search_users():
            search_query = search_entry.get()
            display_users(search_query)

        def go_back():
            users_window.destroy()

        try:
            users_window = tk.Toplevel(root)
            users_window.title("All Users by Role")
            users_window.geometry('950x500')
            users_window.resizable(width=False, height=False)
            users_window.configure(bg="#333333")

            # Search Bar
            search_frame = ttk.Frame(users_window)
            search_frame.pack(pady=5, fill=tk.X)
            ttk.Label(search_frame, text="Search Users:", style="Label.TLabel").pack(side=tk.LEFT, padx=5)
            search_entry = ttk.Entry(search_frame, width=40)
            search_entry.pack(side=tk.LEFT, padx=5)
            ttk.Button(search_frame, text="Search", command=search_users, style="SoftRound.TButton").pack(side=tk.LEFT,
                                                                                                          padx=5)

            # Notebook for roles
            notebook = ttk.Notebook(users_window)
            notebook.pack(pady=10, fill=tk.BOTH, expand=True)

            # Back Button
            ttk.Button(users_window, text="Back", command=go_back, style="SoftRound.TButton").pack(pady=2)

            # Display users initially
            display_users()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch users: {str(e)}")

    # Add Candidate function
    def add_candidate():
        def save_candidate():
            name, party, district = name_entry.get(), party_entry.get(), district_var.get()

            if not all([name, party, district]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                with sqlite3.connect('vo_system.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO candidates (name, party, district, votes) VALUES (?, ?, ?, ?)",
                        (name, party, district, 0)  # Initially, setting votes to 0
                    )
                    conn.commit()

                # Fetch candidate id after insertion to link with dashboard
                cursor.execute("SELECT id FROM candidates WHERE name=?", (name,))
                candidate_id = cursor.fetchone()[0]
                messagebox.showinfo("Success", "Candidate added successfully!")
                add_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add candidate: {str(e)}")

        def go_back():
            add_window.destroy()

        # Create a new window to add a candidate
        add_window = tk.Toplevel(root)
        add_window.title("Add Candidate")
        add_window.geometry('400x350')
        add_window.resizable(False, False)
        add_window.configure(bg="#6495ED")

        # Labels and Entries for Candidate Information
        ttk.Label(add_window, text="Name:", style="Label.TLabel").pack(pady=5)
        name_entry = ttk.Entry(add_window, width=40)
        name_entry.pack(pady=5)

        ttk.Label(add_window, text="Party:", style="Label.TLabel").pack(pady=5)
        party_entry = ttk.Entry(add_window, width=40)
        party_entry.pack(pady=5)

        # Dropdown for District
        district_var = tk.StringVar()
        ttk.Label(add_window, text="District:", style="Label.TLabel").pack(pady=5)
        ttk.Combobox(add_window, textvariable=district_var, values=[
            "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", "Gampaha", "Hambantota",
            "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
            "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura",
            "Trincomalee", "Vavuniya"
        ], state="readonly", width=28).pack(pady=5)

        #save button
        ttk.Button(add_window, text="Save", command=save_candidate, style="SoftRound.TButton").pack(pady=10)
        # Back Button
        ttk.Button(add_window, text="Back", command=go_back, style="SoftRound.TButton").pack(pady=2)
    # Delete Candidate Function
    def delete_candidate():
        def confirm_delete():
            selected_id = candidate_id_entry.get()
            if not selected_id:
                messagebox.showerror("Error", "Please enter a candidate ID to delete.")
                return

            try:
                with sqlite3.connect('vo_system.db') as conn:
                    cursor = conn.cursor()

                    # Check if the candidate exists
                    cursor.execute("SELECT id FROM candidates WHERE id=?", (selected_id,))
                    candidate = cursor.fetchone()

                    if candidate:
                        # Confirm deletion
                        confirm = messagebox.askyesno("Confirm Deletion",
                                                      f"Are you sure you want to delete candidate ID {selected_id}?")
                        if confirm:
                            cursor.execute("DELETE FROM candidates WHERE id=?", (selected_id,))
                            conn.commit()
                            messagebox.showinfo("Success", f"Candidate ID {selected_id} deleted successfully.")
                        else:
                            messagebox.showinfo("Cancelled", "Candidate deletion cancelled.")
                    else:
                        messagebox.showerror("Error", f"No candidate found with ID {selected_id}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete candidate: {str(e)}")

        # Create a new window for deleting a candidate
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Candidate")
        delete_window.geometry('400x200')
        delete_window.resizable(width=False, height=False)
        delete_window.configure(bg="#6495ED")

        ttk.Label(delete_window, text="Enter Candidate ID to delete:", style="Label.TLabel").pack(pady=10)
        candidate_id_entry = ttk.Entry(delete_window, width=30)
        candidate_id_entry.pack(pady=10)
        def go_back():
            delete_window.destroy()
        ttk.Button(delete_window, text="Delete", command=confirm_delete, style="SoftRound.TButton").pack(pady=2)
        # Back Button
        ttk.Button(delete_window, text="Back", command=go_back, style="SoftRound.TButton").pack(pady=2)

    # View Results Function
    def view_results():
        def display_results(search_query=""):
            with sqlite3.connect('vo_system.db') as conn:
                cursor = conn.cursor()
                # Fetch results based on search query
                query = f"%{search_query}%"
                cursor.execute(
                    "SELECT name, party, district, votes FROM candidates WHERE name LIKE ? OR party LIKE ? OR district LIKE ?",
                    (query, query, query),
                )
                results = cursor.fetchall()

            # Clear existing rows in the Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Insert new filtered rows
            for i, result in enumerate(results):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                tree.insert("", tk.END, values=result, tags=(tag,))

        def search_results():
            search_query = search_entry.get()
            display_results(search_query)

        try:
            results_window = tk.Toplevel(root)
            results_window.title("Voting Results")
            results_window.geometry('950x500')
            results_window.resizable(width=False, height=False)
            results_window.configure(bg="#6495ED")
            ttk.Label(results_window, text="Voting Results", style="Header.TLabel").pack(pady=10)

            # Search Bar
            search_frame = ttk.Frame(results_window)
            search_frame.pack(pady=5, fill=tk.X)
            ttk.Label(search_frame, text="Search Results:", style="Label.TLabel").pack(side=tk.LEFT, padx=5)
            search_entry = ttk.Entry(search_frame, width=40)
            search_entry.pack(side=tk.LEFT, padx=5)
            ttk.Button(search_frame, text="Search", command=search_results, style="SoftRound.TButton").pack(
                side=tk.LEFT, padx=5)

            # Treeview for table display
            columns = ("Name", "Party", "District", "Votes")
            tree = ttk.Treeview(results_window, columns=columns, show="headings", style="Treeview")

            # Define headings and column widths
            for col in columns:
                tree.heading(col, text=col, anchor=tk.CENTER)
                tree.column(col, width=200, anchor=tk.CENTER)

            # Add Treeview and scrollbar to frame
            tree.pack(pady=10, fill=tk.BOTH, expand=True)
            scrollbar = ttk.Scrollbar(results_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Display results initially
            display_results()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch results: {str(e)}")

    # Exit Application Function
    def exit_app():
        root.destroy()

    # Buttons
    ttk.Button(frame, text="View Users", command=view_users, style="SoftRound.TButton").grid(row=1, column=0, pady=10)
    ttk.Button(frame, text="Add Candidate", command=add_candidate, style="SoftRound.TButton").grid(row=2, column=0,
                                                                                                   pady=10)
    ttk.Button(frame, text="Delete Candidate", command=delete_candidate, style="SoftRound.TButton").grid(row=3,column=0,pady=10)
    ttk.Button(frame, text="View Results", command=view_results, style="SoftRound.TButton").grid(row=4, column=0,pady=10)
    ttk.Button(frame, text="Exit", command=exit_app, style="SoftRound.TButton").grid(row=5, column=0, pady=10)
    ttk.Button(frame, text="Back", command=lambda: open_page('main_app.py'), style="SoftRound.TButton").grid(row=6,column=0,pady=5)

    root.mainloop()
print(admin())
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os

# Candidate dashboard
def candidate_dashboard(candidate_id):
    root = Tk()
    root.title("Candidate Dashboard")
    root.geometry('950x500')
    root.resizable(False, False)
    root.configure(bg='#6495ED')

    # Apply styles
    style = ttk.Style()
    style.theme_use("clam")

    # Button style
    style.configure("SoftRound.TButton",
                    background="#483D8B",
                    foreground="white",
                    font=("Ubuntu Mono", 12),
                    padding=10,
                    borderwidth=2,
                    relief="flat")
    style.map("SoftRound.TButton",
              background=[("active", "#005a9e")])

    # Header label style
    style.configure("Header.TLabel",
                    font=("Ubuntu Mono", 20, "bold"),
                    background="#6495ED",
                    foreground="#483D8B",
                    padding=5)

    # Label style
    style.configure("Label.TLabel",
                    font=("Ubuntu Mono", 12),
                    background="#6495ED",
                    foreground="#483D8B",
                    padding=5)

    # Treeview style
    style.configure("Treeview",
                    font=("Ubuntu Mono", 12),
                    foreground="#333333",
                    rowheight=25)
    style.configure("Treeview.Heading",
                    font=("Ubuntu Mono", 12, "bold"),
                    background="#333333",
                    foreground="#f9f9f9")

    # Title label
    ttk.Label(root, text="Welcome to the Candidate Dashboard", style="Header.TLabel").pack(pady=10)

    def open_page(page_script):
        root.destroy()  # Close the current window
        os.system(f'python {page_script}')

    # View all candidates' results function
    def view_all_results():
        try:
            with sqlite3.connect('vo_system.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, party, district, votes FROM candidates")
                all_results = cursor.fetchall()

            results_window = Toplevel(root)
            results_window.title("All Candidates Results")
            results_window.geometry("950x500")
            results_window.configure(bg='#6495ED')

            ttk.Label(results_window, text="All Candidates Voting Results", style="Header.TLabel").pack(pady=10)

            # Treeview setup
            tree = ttk.Treeview(results_window, columns=("Name", "Party", "District", "Votes"), show="headings")
            tree.pack(padx=20, pady=20, fill=BOTH, expand=True)

            # Define column headings
            tree.heading("Name", text="Name")
            tree.heading("Party", text="Party")
            tree.heading("District", text="District")
            tree.heading("Votes", text="Votes")

            # Define column widths
            tree.column("Name", width=200)
            tree.column("Party", width=150)
            tree.column("District", width=150)
            tree.column("Votes", width=100)

            # Insert the results into the treeview
            for result in all_results:
                tree.insert("", "end", values=result)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch all results: {str(e)}")

    # Function to update user profile
    def update_user_profile(user_id):
        def save_changes():
            new_password = entry_password.get()
            new_email = entry_email.get()
            new_district = combo_district.get()

            try:
                conn = sqlite3.connect('vo_system.db')
                cursor = conn.cursor()

                # Update password if provided
                if new_password:
                    cursor.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))

                # Update email if provided
                if new_email:
                    cursor.execute("UPDATE users SET email=? WHERE id=?", (new_email, user_id))

                # Update district if provided
                if new_district:
                    cursor.execute("UPDATE users SET district=? WHERE id=?", (new_district, user_id))

                conn.commit()
                messagebox.showinfo("Success", "Profile updated successfully!")
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()

        # Profile update window
        update_window = Toplevel(root)
        update_window.title("Update Profile")
        update_window.geometry("400x350")
        update_window.configure(bg='#6495ED')

        ttk.Label(update_window, text="Update Your Profile", style="Header.TLabel").pack(pady=10)

        # Entry fields for password, email, and district
        ttk.Label(update_window, text="New Password", style="Label.TLabel").pack(pady=5)
        entry_password = ttk.Entry(update_window, style="TEntry", show="*")
        entry_password.pack(pady=5)

        ttk.Label(update_window, text="New Email", style="Label.TLabel").pack(pady=5)
        entry_email = ttk.Entry(update_window, style="TEntry")
        entry_email.pack(pady=5)

        ttk.Label(update_window, text="New District", style="Label.TLabel").pack(pady=5)
        combo_district = ttk.Combobox(update_window, values=[
            "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", "Gampaha", "Hambantota", "Jaffna",
            "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale", "Matara", "Monaragala",
            "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya"], style="TCombobox")
        combo_district.pack(pady=5)

        # Save button
        ttk.Button(update_window, text="Save Changes", style="SoftRound.TButton", command=save_changes).pack(pady=10)

    # Buttons for the dashboard
    ttk.Button(root, text="View All Candidates Results", style="SoftRound.TButton", command=view_all_results).pack(pady=10)
    ttk.Button(root, text="Update Profile", style="SoftRound.TButton", command=lambda: update_user_profile(candidate_id)).pack(pady=20)
    ttk.Button(root, text="Back", style="SoftRound.TButton", command=lambda: open_page('main_app.py')).pack(pady=10)

    root.mainloop()

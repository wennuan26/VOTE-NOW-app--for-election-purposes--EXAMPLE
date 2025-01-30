import sqlite3

# Create database and tables
conn = sqlite3.connect('vo_system.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''CREATE TABLE Users (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    name TEXT NOT NULL,
    nic TEXT UNIQUE NOT NULL CHECK(LENGTH(nic) <= 10),
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    district TEXT
)''')

# Create Candidates table
cursor.execute('''CREATE TABLE Candidates (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    name TEXT NOT NULL,
    party TEXT NOT NULL,
    district TEXT NOT NULL,
    votes INTEGER DEFAULT 0
)''')

# Create Votes table
cursor.execute('''CREATE TABLE Votes (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
)''')

# Add default admin user
cursor.execute("SELECT * FROM Users WHERE role = 'Admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (name, nic, email, password, role, district) VALUES (?, ?, ?, ?, ?, ?)",
                   ("AdminChei", "123456789V", "adminchei@example.com", "adminchei123", "Admin", "Colombo"))

conn.commit()
conn.close()

print("Database setup complete.")

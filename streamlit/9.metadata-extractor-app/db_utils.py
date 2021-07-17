# Database Management
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


# Table
def create_uploaded_file_table():
    c.execute("""
    CREATE TABLE IF NOT EXISTS files_table(filename TEXT, 
    filetype TEXT, filesize TEXT, upload_date TIMESTAMP)
    """)


# Adding Details
def add_file_details(filename, filetype, filesize, upload_date):
    c.execute(f"""
    INSERT INTO files_table(filename, filetype, filesize, upload_date)
    VALUES (?, ?, ?, ?)
    """, (filename, filetype, filesize, upload_date))
    conn.commit()


# View Details
def view_all_data():
    c.execute("""
    SELECT * FROM files_table
    """)
    data = c.fetchall()
    return data

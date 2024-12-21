import os

os.add_dll_directory(r"C:\Program Files\PostgreSQL\16\bin")

import psycopg2

try:
    conn = psycopg2.connect(
        dbname = "projects",
        user = "aman_m",
        password = "aman20015",
        host = "127.0.0.1",
        port = "5432"
    )

except psycopg2.Error:
    print("No connection to database")

else:
    cursor = conn.cursor()
    
    

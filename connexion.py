import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="school_management",
        user="kader",
        password="password"
    )
    return conn

import mysql.connector
from mysql.connector import Error

from db_config import DB_CONFIG


def get_connection():
    """Open a new connection to the job_portal MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    """Create the database (if it doesn't exist yet) and all tables."""

    try:
        config_no_db = {k: v for k, v in DB_CONFIG.items() if k != "database"}
        server_conn = mysql.connector.connect(**config_no_db)
        server_cursor = server_conn.cursor()
        server_cursor.execute(
            "CREATE DATABASE IF NOT EXISTS " + DB_CONFIG["database"]
        )
        server_conn.commit()
        server_cursor.close()
        server_conn.close()
    except Error as e:
        print("\n[Database Error] Could not connect to MySQL server.")
        print("Details:", e)
        print("Check the settings in db_config.py and make sure MySQL is running.\n")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                role VARCHAR(50),
                phone VARCHAR(50),
                qualification VARCHAR(255),
                skills TEXT,
                experience VARCHAR(255),
                resume VARCHAR(500),
                resume_text TEXT,
                location VARCHAR(255),
                company_name VARCHAR(255),
                company_description TEXT,
                company_location VARCHAR(255),
                company_website VARCHAR(255),
                company_email VARCHAR(255),
                company_phone VARCHAR(50),
                verified VARCHAR(10)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INT PRIMARY KEY,
                recruiter_id INT,
                company_name VARCHAR(255),
                job_title VARCHAR(255),
                description TEXT,
                skills TEXT,
                qualification VARCHAR(255),
                experience VARCHAR(255),
                salary VARCHAR(100),
                location VARCHAR(255),
                status VARCHAR(50)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                application_id INT PRIMARY KEY,
                job_id INT,
                candidate_id INT,
                resume VARCHAR(500),
                status VARCHAR(50),
                status_reason TEXT
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    except Error as e:
        print("\n[Database Error] Could not set up tables.")
        print("Details:", e, "\n")
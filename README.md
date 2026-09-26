# Job Application Portal

A command-line job application portal with three roles: Job Seeker,
Recruiter, and Administrator.

## Data storage

All data (users, jobs, applications) is stored in a **MySQL** database
instead of files. The app creates the database and tables automatically
the first time it runs, as long as it can connect to your MySQL server.

## Setup

1. Install MySQL Server and make sure it is running.
2. Install the Python dependency:
   ```
   pip install -r requirements.txt
   ```
3. Open `db_config.py` and set your MySQL host, username and password.
   (You do not need to create the `job_portal` database yourself - the
   app creates it on first run.)
4. Run the app:
   ```
   python main.py
   ```

If the connection fails, the app prints a `[Database Error]` message
with details instead of crashing - double check `db_config.py` and
that MySQL is running.

## Notes

- `users.csv` is no longer used; it is kept only as a reference to the
  previous file-based version of this project. All data now lives in
  the `users`, `jobs`, and `applications` tables in MySQL.
- The default admin login is `admin@gmail.com` / `admin123`, created
  automatically on first run.

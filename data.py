from mysql.connector import Error
from connection import get_connection, init_db


users = []
jobs = []
applications = []


class User:

    def __init__(self, user_id, name, email, password, role):

        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

        self.phone = ""
        self.qualification = ""
        self.skills = ""
        self.experience = ""
        self.resume = ""
        self.resume_text = ""
        self.location = ""

        self.company_name = ""
        self.company_description = ""
        self.company_location = ""
        self.company_website = ""
        self.company_email = ""
        self.company_phone = ""
        self.verified = "No"


class Job:

    def __init__(
        self,
        job_id,
        recruiter_id,
        company_name,
        job_title,
        description,
        skills,
        qualification,
        experience,
        salary,
        location
    ):

        self.job_id = job_id
        self.recruiter_id = recruiter_id
        self.company_name = company_name
        self.job_title = job_title
        self.description = description
        self.skills = skills
        self.qualification = qualification
        self.experience = experience
        self.salary = salary
        self.location = location
        self.status = "Open"


class Application:

    def __init__(
        self,
        application_id,
        job_id,
        candidate_id,
        resume
    ):

        self.application_id = application_id
        self.job_id = job_id
        self.candidate_id = candidate_id
        self.resume = resume
        self.status = "Applied"
        self.status_reason = ""


USER_FIELDS = [
    "user_id",
    "name",
    "email",
    "password",
    "role",
    "phone",
    "qualification",
    "skills",
    "experience",
    "resume",
    "resume_text",
    "location",
    "company_name",
    "company_description",
    "company_location",
    "company_website",
    "company_email",
    "company_phone",
    "verified",
]

JOB_FIELDS = [
    "job_id",
    "recruiter_id",
    "company_name",
    "job_title",
    "description",
    "skills",
    "qualification",
    "experience",
    "salary",
    "location",
    "status",
]

APPLICATION_FIELDS = [
    "application_id",
    "job_id",
    "candidate_id",
    "resume",
    "status",
    "status_reason",
]


# users 

def load_users():

    users.clear()

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not load users:", e)
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT " + ", ".join(USER_FIELDS) + " FROM users")

    for row in cursor.fetchall():

        user = User(
            row["user_id"],
            row["name"],
            row["email"],
            row["password"],
            row["role"]
        )

        for field in USER_FIELDS[5:]:
            setattr(user, field, row.get(field) or "")

        users.append(user)

    cursor.close()
    conn.close()


def save_users():

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not save users:", e)
        return

    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(USER_FIELDS))
    updates = ", ".join(f"{field}=VALUES({field})" for field in USER_FIELDS[1:])

    query = (
        "INSERT INTO users (" + ", ".join(USER_FIELDS) + ") "
        "VALUES (" + placeholders + ") "
        "ON DUPLICATE KEY UPDATE " + updates
    )

    for user in users:
        cursor.execute(query, [getattr(user, field) for field in USER_FIELDS])

    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_id(user_id):

    for user in users:

        if user.user_id == user_id:
            return user

    return None


#  jobs

def load_jobs():

    jobs.clear()

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not load jobs:", e)
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT " + ", ".join(JOB_FIELDS) + " FROM jobs ORDER BY job_id")

    for row in cursor.fetchall():

        job = Job(
            row["job_id"],
            row["recruiter_id"],
            row["company_name"],
            row["job_title"],
            row["description"],
            row["skills"],
            row["qualification"],
            row["experience"],
            row["salary"],
            row["location"]
        )
        job.status = row.get("status") or "Open"

        jobs.append(job)

    cursor.close()
    conn.close()


def save_jobs():

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not save jobs:", e)
        return

    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(JOB_FIELDS))
    updates = ", ".join(f"{field}=VALUES({field})" for field in JOB_FIELDS[1:])

    query = (
        "INSERT INTO jobs (" + ", ".join(JOB_FIELDS) + ") "
        "VALUES (" + placeholders + ") "
        "ON DUPLICATE KEY UPDATE " + updates
    )

    for job in jobs:
        cursor.execute(query, [getattr(job, field) for field in JOB_FIELDS])

    conn.commit()
    cursor.close()
    conn.close()


def delete_job(job_id):

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not delete job:", e)
        return

    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
    conn.commit()
    cursor.close()
    conn.close()


# applications 

def load_applications():

    applications.clear()

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not load applications:", e)
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT " + ", ".join(APPLICATION_FIELDS) + " FROM applications ORDER BY application_id"
    )

    for row in cursor.fetchall():

        application = Application(
            row["application_id"],
            row["job_id"],
            row["candidate_id"],
            row["resume"]
        )
        application.status = row.get("status") or "Applied"
        application.status_reason = row.get("status_reason") or ""

        applications.append(application)

    cursor.close()
    conn.close()


def save_applications():

    try:
        conn = get_connection()
    except Error as e:
        print("[Database Error] Could not save applications:", e)
        return

    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(APPLICATION_FIELDS))
    updates = ", ".join(f"{field}=VALUES({field})" for field in APPLICATION_FIELDS[1:])

    query = (
        "INSERT INTO applications (" + ", ".join(APPLICATION_FIELDS) + ") "
        "VALUES (" + placeholders + ") "
        "ON DUPLICATE KEY UPDATE " + updates
    )

    for application in applications:
        cursor.execute(
            query, [getattr(application, field) for field in APPLICATION_FIELDS]
        )

    conn.commit()
    cursor.close()
    conn.close()


def change_status(application, status, reason=""):

    application.status = status
    application.status_reason = reason
    save_applications()


init_db()
load_users()
load_jobs()
load_applications()
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
        self.location = ""

        self.company_name = ""
        self.company_description = ""
        self.company_location = ""
        self.company_website = ""
        self.company_email = ""


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
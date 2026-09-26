from data import (
    users,
    jobs,
    applications,
    Application,
    save_users,
    save_applications,
    get_user_by_id,
)
from validation import input_email, input_phone, input_skills, input_resume
from matching import skill_match, print_skill_match

RESUME_TEXT_LIMIT = 3000


def create_profile(candidate):

    print("\nProfile Creation")

    candidate.name = input("Full name: ")
    candidate.email = input_email("Email: ")
    candidate.phone = input_phone("Phone number: ")
    candidate.qualification = input("Qualification: ")
    candidate.skills = input_skills("Skills: ")
    candidate.experience = input("Experience: ")

    resume_path, resume_text = input_resume("Resume file path (PDF): ")
    candidate.resume = resume_path
    candidate.resume_text = resume_text[:RESUME_TEXT_LIMIT]

    candidate.location = input("Location: ")

    save_users()

    print("\nProfile created successfully!")

    check_resume_skills(candidate)


def profile_score(candidate):
    """Profile completeness: percentage of fields filled in (no photo)."""

    fields = {
        "Name": candidate.name,
        "Email": candidate.email,
        "Phone": candidate.phone,
        "Qualification": candidate.qualification,
        "Skills": candidate.skills,
        "Experience": candidate.experience,
        "Resume": candidate.resume,
        "Location": candidate.location,
    }

    filled = [name for name, value in fields.items() if value.strip() != ""]
    missing = [name for name in fields if name not in filled]

    percent = round(len(filled) / len(fields) * 100)

    return percent, missing


def check_resume_skills(candidate):
    """Compare the skills the candidate listed against the words actually
    found inside their uploaded resume PDF."""

    if candidate.resume_text.strip() == "":
        return

    if candidate.skills.strip() == "":
        return

    resume_lower = candidate.resume_text.lower()

    listed = [s.strip() for s in candidate.skills.split(",") if s.strip()]

    found = [s for s in listed if s.lower() in resume_lower]
    not_found = [s for s in listed if s.lower() not in resume_lower]

    print("\nResume Check")
    print("Skills found in resume:", ", ".join(found) if found else "None")

    if not_found:
        print(
            "Listed but not found in resume text (consider adding these "
            "to your resume):",
            ", ".join(not_found)
        )


def view_profile(candidate):

    print("\nMy Profile")

    print("Name:", candidate.name)
    print("Email:", candidate.email)
    print("Phone:", candidate.phone)
    print("Qualification:", candidate.qualification)
    print("Skills:", candidate.skills)
    print("Experience:", candidate.experience)
    print("Resume:", candidate.resume)
    print("Location:", candidate.location)

    percent, missing = profile_score(candidate)
    print("\nProfile Strength:", str(percent) + "%")

    if missing:
        print("Complete these fields to improve your score:", ", ".join(missing))

    check_resume_skills(candidate)


def print_job_verified(job):

    recruiter = get_user_by_id(job.recruiter_id)
    verified = recruiter.verified if recruiter else "No"

    print("Verified Company:", "Yes" if verified == "Yes" else "No")


def search_jobs(candidate=None):

    print("\nJob Search")

    if len(jobs) == 0:
        print("No jobs available.")
        return

    search = input("Enter job title, skill or location: ").lower()

    found = False

    for job in jobs:

        if (
            search in job.job_title.lower()
            or search in job.skills.lower()
            or search in job.location.lower()
        ):

            found = True

            print("\nJob ID:", job.job_id)
            print("Company:", job.company_name)
            print("Job:", job.job_title)
            print("Description:", job.description)
            print("Skills:", job.skills)
            print("Qualification:", job.qualification)
            print("Experience:", job.experience)
            print("Salary:", job.salary)
            print("Location:", job.location)
            print("Status:", job.status)
            print_job_verified(job)

            if candidate is not None and candidate.skills.strip() != "":
                print_skill_match(candidate.skills, job.skills)

    if not found:
        print("No matching jobs found.")


def view_all_jobs(candidate=None):

    print("\nAvailable Jobs")

    if len(jobs) == 0:
        print("No jobs available.")
        return

    for job in jobs:

        print("\nJob ID:", job.job_id)
        print("Company:", job.company_name)
        print("Job:", job.job_title)
        print("Description:", job.description)
        print("Skills:", job.skills)
        print("Qualification:", job.qualification)
        print("Experience:", job.experience)
        print("Salary:", job.salary)
        print("Location:", job.location)
        print("Status:", job.status)
        print_job_verified(job)

        if candidate is not None and candidate.skills.strip() != "":
            print_skill_match(candidate.skills, job.skills)


def apply_job(candidate):

    print("\nJob Application")

    view_all_jobs(candidate)

    try:
        job_id = int(input("\nEnter Job ID to apply: "))
    except ValueError:
        print("Invalid Job ID.")
        return

    selected_job = None

    for job in jobs:

        if job.job_id == job_id:
            selected_job = job
            break

    if selected_job is None:
        print("Job not found.")
        return

    if selected_job.status != "Open":
        print("This job is currently closed.")
        return

    for application in applications:

        if (
            application.job_id == job_id
            and application.candidate_id == candidate.user_id
        ):

            print("You have already applied for this job.")
            return

    if candidate.resume == "":
        print("Please create your profile and add your resume first.")
        return

    if candidate.skills.strip() != "":

        print()
        print_skill_match(candidate.skills, selected_job.skills)

        confirm = input("\nProceed with this application? (y/n): ").lower()

        if confirm != "y":
            print("Application cancelled.")
            return

    if len(applications) == 0:
        application_id = 1
    else:
        application_id = applications[-1].application_id + 1

    new_application = Application(
        application_id,
        job_id,
        candidate.user_id,
        candidate.resume
    )

    applications.append(new_application)
    save_applications()

    print("\nApplication submitted successfully!")
    print("Application ID:", application_id)
    print("Job:", selected_job.job_title)
    print("Company:", selected_job.company_name)


def my_applications(candidate):

    print("\nMy Applications")

    found = False

    for application in applications:

        if application.candidate_id == candidate.user_id:

            found = True
            job = None

            for j in jobs:

                if j.job_id == application.job_id:
                    job = j
                    break

            if job is not None:

                print("\nApplication ID:", application.application_id)
                print("Company:", job.company_name)
                print("Job:", job.job_title)
                print("Location:", job.location)
                print("Resume:", application.resume)
                print("Status:", application.status)

                if application.status_reason:
                    print("Reason:", application.status_reason)

    if not found:
        print("You have not applied for any jobs.")


def application_status(candidate):

    print("\nApplication Status")

    found = False

    for application in applications:

        if application.candidate_id == candidate.user_id:

            found = True
            job = None

            for j in jobs:

                if j.job_id == application.job_id:
                    job = j
                    break

            if job is not None:

                print("\nApplication ID:", application.application_id)
                print("Job:", job.job_title)
                print("Company:", job.company_name)
                print("Status:", application.status)

                if application.status_reason:
                    print("Reason:", application.status_reason)

    if not found:
        print("No applications found.")


def withdraw_application(candidate):

    print("\nWithdraw Application")

    my_applications(candidate)

    try:
        application_id = int(
            input("\nEnter Application ID to withdraw: ")
        )
    except ValueError:
        print("Invalid Application ID.")
        return

    for application in applications:

        if (
            application.application_id == application_id
            and application.candidate_id == candidate.user_id
        ):

            if application.status in ["Selected", "Rejected"]:
                print("You cannot withdraw this application.")
                return

            application.status = "Withdrawn"
            save_applications()

            print("\nApplication withdrawn successfully!")
            return

    print("Application not found.")


def candidate_menu(candidate):

    while True:

        print("\nJob Seeker Dashboard")
        print("1. Create Profile")
        print("2. View Profile")
        print("3. Search Jobs")
        print("4. View All Jobs")
        print("5. Apply for Job")
        print("6. My Applications")
        print("7. Application Status")
        print("8. Withdraw Application")
        print("9. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":
            create_profile(candidate)

        elif choice == "2":
            view_profile(candidate)

        elif choice == "3":
            search_jobs(candidate)

        elif choice == "4":
            view_all_jobs(candidate)

        elif choice == "5":
            apply_job(candidate)

        elif choice == "6":
            my_applications(candidate)

        elif choice == "7":
            application_status(candidate)

        elif choice == "8":
            withdraw_application(candidate)

        elif choice == "9":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
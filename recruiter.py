from data import users, jobs, applications, Job


def post_job(recruiter):
    print("\nPost Job")

    company_name = input("Company name: ")
    job_title = input("Job title: ")
    description = input("Job description: ")
    skills = input("Required skills: ")
    qualification = input("Qualification: ")
    experience = input("Experience: ")
    salary = input("Salary: ")
    location = input("Location: ")

    if len(jobs) == 0:
        job_id = 1
    else:
        job_id = jobs[-1].job_id + 1

    new_job = Job(
        job_id,
        recruiter.user_id,
        company_name,
        job_title,
        description,
        skills,
        qualification,
        experience,
        salary,
        location
    )

    jobs.append(new_job)

    print("\nJob posted successfully!")
    print("Job ID:", job_id)


def recruiter_jobs(recruiter):
    print("\nMy Job Postings")

    found = False

    for job in jobs:
        if job.recruiter_id == recruiter.user_id:
            found = True

            print("\nJob ID:", job.job_id)
            print("Company:", job.company_name)
            print("Job:", job.job_title)
            print("Location:", job.location)
            print("Status:", job.status)
            print("-" * 40)

    if not found:
        print("You have not posted any jobs.")


def recruiter_applications(recruiter):
    print("\nApplications")

    found = False

    for application in applications:
        for job in jobs:
            if (job.job_id == application.job_id and
                    job.recruiter_id == recruiter.user_id):

                found = True
                candidate = None

                for user in users:
                    if user.user_id == application.candidate_id:
                        candidate = user
                        break

                print("\nApplication ID:", application.application_id)
                print("Job:", job.job_title)
                print("Candidate:", candidate.name)
                print("Email:", candidate.email)
                print("Resume:", application.resume)
                print("Status:", application.status)
                print("-" * 40)

    if not found:
        print("No applications received.")


def update_application_status(recruiter):
    recruiter_applications(recruiter)

    try:
        application_id = int(input("\nEnter Application ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for application in applications:
        if application.application_id == application_id:

            for job in jobs:
                if (job.job_id == application.job_id and
                        job.recruiter_id == recruiter.user_id):

                    print("\nSelect Status")
                    print("1. Under Review")
                    print("2. Shortlisted")
                    print("3. Rejected")
                    print("4. Selected")

                    choice = input("Enter choice: ")

                    status_dict = {
                        "1": "Under Review",
                        "2": "Shortlisted",
                        "3": "Rejected",
                        "4": "Selected"
                    }

                    if choice in status_dict:
                        application.status = status_dict[choice]
                        print("\nApplication status updated!")
                    else:
                        print("Invalid status.")

                    return

    print("Application not found.")


def recruiter_menu(recruiter):
    while True:
        print("\nRecruiter Dashboard")
        print("1. Post Job")
        print("2. My Job Postings")
        print("3. View Applications")
        print("4. Update Application Status")
        print("5. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":
            post_job(recruiter)

        elif choice == "2":
            recruiter_jobs(recruiter)

        elif choice == "3":
            recruiter_applications(recruiter)

        elif choice == "4":
            update_application_status(recruiter)

        elif choice == "5":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
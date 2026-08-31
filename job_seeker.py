from data import users, jobs, applications, Application


def view_jobs():
    print("\nAvailable Jobs")

    if len(jobs) == 0:
        print("No jobs available.")
        return

    for job in jobs:
        if job.status == "Open":
            print("\nJob ID:", job.job_id)
            print("Company:", job.company_name)
            print("Job Title:", job.job_title)
            print("Description:", job.description)
            print("Skills:", job.skills)
            print("Qualification:", job.qualification)
            print("Experience:", job.experience)
            print("Salary:", job.salary)
            print("Location:", job.location)
            print("Status:", job.status)


def view_job_details():
    view_jobs()

    try:
        job_id = int(input("\nEnter Job ID: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for job in jobs:
        if job.job_id == job_id:
            print("\nJob Details")
            print("Company:", job.company_name)
            print("Job Title:", job.job_title)
            print("Description:", job.description)
            print("Required Skills:", job.skills)
            print("Qualification:", job.qualification)
            print("Experience:", job.experience)
            print("Salary:", job.salary)
            print("Location:", job.location)
            print("Status:", job.status)
            return

    print("Job not found.")


def apply_for_job(candidate):
    view_jobs()

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
        print("This job is closed.")
        return

    for application in applications:
        if (
            application.job_id == job_id
            and application.candidate_id == candidate.user_id
        ):
            print("You have already applied for this job.")
            return

    resume = input("Enter resume file name: ")

    application_id = len(applications) + 1

    new_application = Application(
        application_id,
        job_id,
        candidate.user_id,
        resume
    )

    applications.append(new_application)

    print("\nApplication submitted successfully!")


def candidate_applications(candidate):
    print("\nMy Applications")

    found = False

    for application in applications:
        if application.candidate_id == candidate.user_id:
            found = True

            for job in jobs:
                if job.job_id == application.job_id:
                    print("\nApplication ID:", application.application_id)
                    print("Job:", job.job_title)
                    print("Company:", job.company_name)
                    print("Resume:", application.resume)
                    print("Status:", application.status)

    if not found:
        print("No applications found.")


def candidate_profile(candidate):
    print("\nCandidate Profile")
    print("User ID:", candidate.user_id)
    print("Name:", candidate.name)
    print("Email:", candidate.email)
    print("Role:", candidate.role)


def candidate_menu(candidate):
    while True:
        print("\nJob Seeker Dashboard")
        print("1. View Jobs")
        print("2. View Job Details")
        print("3. Apply for Job")
        print("4. My Applications")
        print("5. My Profile")
        print("6. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":
            view_jobs()

        elif choice == "2":
            view_job_details()

        elif choice == "3":
            apply_for_job(candidate)

        elif choice == "4":
            candidate_applications(candidate)

        elif choice == "5":
            candidate_profile(candidate)

        elif choice == "6":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
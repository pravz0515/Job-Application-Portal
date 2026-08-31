from data import users, jobs, applications, Job


def company_profile_setup(recruiter):

    print("\nCompany Profile Setup")

    recruiter.company_name = input("Company name: ")
    recruiter.company_description = input("Company description: ")
    recruiter.company_location = input("Company location: ")
    recruiter.company_website = input("Company website: ")
    recruiter.company_email = input("Company email: ")

    print("\nCompany profile created successfully!")


def view_company_profile(recruiter):

    print("\nCompany Profile")

    if recruiter.company_name == "":
        print("Company profile is not created yet.")
        return

    print("Company Name:", recruiter.company_name)
    print("Description:", recruiter.company_description)
    print("Location:", recruiter.company_location)
    print("Website:", recruiter.company_website)
    print("Email:", recruiter.company_email)


def post_job(recruiter):

    print("\nPost Job")

    if recruiter.company_name == "":
        print("Please setup company profile first.")
        return

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
        recruiter.company_name,
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

    if not found:
        print("You have not posted any jobs.")


def recruiter_applications(recruiter):

    print("\nReceived Applications")

    found = False

    for application in applications:

        for job in jobs:

            if (
                job.job_id == application.job_id
                and job.recruiter_id == recruiter.user_id
            ):

                found = True
                candidate = None

                for user in users:

                    if user.user_id == application.candidate_id:
                        candidate = user
                        break

                if candidate is not None:

                    print("\nApplication ID:", application.application_id)
                    print("Job:", job.job_title)
                    print("Candidate:", candidate.name)
                    print("Email:", candidate.email)
                    print("Phone:", candidate.phone)
                    print("Qualification:", candidate.qualification)
                    print("Skills:", candidate.skills)
                    print("Experience:", candidate.experience)
                    print("Resume:", application.resume)
                    print("Status:", application.status)

    if not found:
        print("No applications received.")


def review_candidate(recruiter):

    print("\nReview Candidates")

    found = False

    for application in applications:

        for job in jobs:

            if (
                job.job_id == application.job_id
                and job.recruiter_id == recruiter.user_id
            ):

                found = True
                candidate = None

                for user in users:

                    if user.user_id == application.candidate_id:
                        candidate = user
                        break

                if candidate is not None:

                    print("\nApplication ID:", application.application_id)
                    print("Candidate:", candidate.name)
                    print("Email:", candidate.email)
                    print("Qualification:", candidate.qualification)
                    print("Skills:", candidate.skills)
                    print("Experience:", candidate.experience)
                    print("Resume:", application.resume)
                    print("Job:", job.job_title)
                    print("Current Status:", application.status)

    if not found:
        print("No candidates available for review.")


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

                if (
                    job.job_id == application.job_id
                    and job.recruiter_id == recruiter.user_id
                ):

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
                        print("New Status:", application.status)

                    else:
                        print("Invalid status.")

                    return

    print("Application not found.")


def shortlist_candidate(recruiter):

    print("\nShortlist Candidate")

    recruiter_applications(recruiter)

    try:
        application_id = int(input("\nEnter Application ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for application in applications:

        if application.application_id == application_id:

            for job in jobs:

                if (
                    job.job_id == application.job_id
                    and job.recruiter_id == recruiter.user_id
                ):

                    application.status = "Shortlisted"

                    print("\nCandidate shortlisted successfully!")
                    return

    print("Application not found.")


def reject_candidate(recruiter):

    print("\nReject Candidate")

    recruiter_applications(recruiter)

    try:
        application_id = int(input("\nEnter Application ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for application in applications:

        if application.application_id == application_id:

            for job in jobs:

                if (
                    job.job_id == application.job_id
                    and job.recruiter_id == recruiter.user_id
                ):

                    application.status = "Rejected"

                    print("\nCandidate rejected.")
                    return

    print("Application not found.")


def select_candidate(recruiter):

    print("\nSelect Candidate")

    recruiter_applications(recruiter)

    try:
        application_id = int(input("\nEnter Application ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for application in applications:

        if application.application_id == application_id:

            for job in jobs:

                if (
                    job.job_id == application.job_id
                    and job.recruiter_id == recruiter.user_id
                ):

                    application.status = "Selected"

                    print("\nCandidate selected successfully!")
                    return

    print("Application not found.")


def recruiter_menu(recruiter):

    while True:

        print("\nRecruiter Dashboard")
        print("1. Company Profile Setup")
        print("2. View Company Profile")
        print("3. Post Job")
        print("4. My Job Postings")
        print("5. Receive Applications")
        print("6. Review Candidates")
        print("7. Shortlist Candidate")
        print("8. Reject Candidate")
        print("9. Select Candidate")
        print("10. Update Application Status")
        print("11. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":
            company_profile_setup(recruiter)

        elif choice == "2":
            view_company_profile(recruiter)

        elif choice == "3":
            post_job(recruiter)

        elif choice == "4":
            recruiter_jobs(recruiter)

        elif choice == "5":
            recruiter_applications(recruiter)

        elif choice == "6":
            review_candidate(recruiter)

        elif choice == "7":
            shortlist_candidate(recruiter)

        elif choice == "8":
            reject_candidate(recruiter)

        elif choice == "9":
            select_candidate(recruiter)

        elif choice == "10":
            update_application_status(recruiter)

        elif choice == "11":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
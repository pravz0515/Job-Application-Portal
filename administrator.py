from data import users, jobs, applications, save_users, delete_job


def admin_users():

    print("\nAll Users")

    if len(users) == 0:
        print("No users found.")
        return

    for user in users:

        print(
            user.user_id,
            "|",
            user.name,
            "|",
            user.email,
            "|",
            user.role,
            "|",
            ("Verified" if user.verified == "Yes" else "Not Verified")
            if user.role == "recruiter" else ""
        )


def admin_jobs():

    print("\nAll Jobs")

    if len(jobs) == 0:
        print("No jobs found.")
        return

    for job in jobs:

        print(
            job.job_id,
            "|",
            job.company_name,
            "|",
            job.job_title,
            "|",
            job.status
        )


def admin_applications():

    print("\nAll Applications")

    if len(applications) == 0:
        print("No applications found.")
        return

    for application in applications:

        print("\nApplication ID:", application.application_id)
        print("Job ID:", application.job_id)
        print("Candidate ID:", application.candidate_id)
        print("Status:", application.status)


def admin_verify_company():

    print("\nCompany Verification")

    recruiters = [u for u in users if u.role == "recruiter" and u.company_name != ""]

    if len(recruiters) == 0:
        print("No company profiles found.")
        return

    for user in recruiters:
        print(
            user.user_id,
            "|",
            user.company_name,
            "|",
            "Verified" if user.verified == "Yes" else "Not Verified"
        )

    try:
        user_id = int(input("\nEnter User ID to verify/unverify: "))
    except ValueError:
        print("Invalid User ID.")
        return

    for user in recruiters:

        if user.user_id == user_id:

            print("1. Mark as Verified")
            print("2. Mark as Not Verified")

            choice = input("Enter choice: ")

            if choice == "1":
                user.verified = "Yes"
                print("\nCompany marked as verified.")

            elif choice == "2":
                user.verified = "No"
                print("\nCompany marked as not verified.")

            else:
                print("Invalid choice.")
                return

            save_users()
            return

    print("User not found.")


def admin_remove_job():

    print("\nRemove Job Posting")

    admin_jobs()

    if len(jobs) == 0:
        return

    try:
        job_id = int(input("\nEnter Job ID to remove: "))
    except ValueError:
        print("Invalid Job ID.")
        return

    for job in jobs:

        if job.job_id == job_id:
            jobs.remove(job)
            delete_job(job.job_id)
            print("\nJob posting removed.")
            return

    print("Job not found.")


def admin_menu(admin):

    while True:

        print("\nAdministrator Dashboard")
        print("1. View Users")
        print("2. View Jobs")
        print("3. View Applications")
        print("4. Verify/Unverify Company")
        print("5. Remove Job Posting")
        print("6. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":
            admin_users()

        elif choice == "2":
            admin_jobs()

        elif choice == "3":
            admin_applications()

        elif choice == "4":
            admin_verify_company()

        elif choice == "5":
            admin_remove_job()

        elif choice == "6":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
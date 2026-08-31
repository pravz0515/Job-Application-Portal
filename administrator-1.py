from data import users, jobs, applications


def admin_users():
    print("\nAll Users")

    if len(users) == 0:
        print("No users found.")
        return

    for user in users:
        print(
            user.user_id, "|",
            user.name, "|",
            user.email, "|",
            user.role
        )


def admin_jobs():
    print("\nAll Jobs")

    if len(jobs) == 0:
        print("No jobs found.")
        return

    for job in jobs:
        print(
            job.job_id, "|",
            job.company_name, "|",
            job.job_title, "|",
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


def admin_menu(admin):
    while True:
        print("\nAdministrator Dashboard")
        print("1. View Users")
        print("2. View Jobs")
        print("3. View Applications")
        print("4. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":
            admin_users()

        elif choice == "2":
            admin_jobs()

        elif choice == "3":
            admin_applications()

        elif choice == "4":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
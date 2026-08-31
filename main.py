from data import users, User

from job_seeker import candidate_menu
from recruiter import recruiter_menu
from administrator import admin_menu


def register():

    print("\nRegister")

    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    print("\nSelect Role")
    print("1. Job Seeker")
    print("2. Recruiter")

    choice = input("Enter choice: ")

    if choice == "1":
        role = "candidate"

    elif choice == "2":
        role = "recruiter"

    else:
        print("Invalid role.")
        return

    for user in users:

        if user.email == email:
            print("Email already registered.")
            return

    user_id = len(users) + 1

    new_user = User(
        user_id,
        name,
        email,
        password,
        role
    )

    users.append(new_user)

    print("\nRegistration successful!")


def login():

    print("\nLogin")

    email = input("Enter email: ")
    password = input("Enter password: ")

    for user in users:

        if user.email == email and user.password == password:

            print("\nLogin successful!")

            if user.role == "candidate":
                candidate_menu(user)

            elif user.role == "recruiter":
                recruiter_menu(user)

            elif user.role == "admin":
                admin_menu(user)

            return

    print("\nInvalid email or password.")


def create_admin():

    for user in users:

        if user.role == "admin":
            return

    admin = User(
        0,
        "Administrator",
        "admin@gmail.com",
        "admin123",
        "admin"
    )

    users.append(admin)


def main():

    create_admin()

    while True:

        print("\nJOB APPLICATION PORTAL")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            login()

        elif choice == "3":
            print("\nThank you for using Job Application Portal.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
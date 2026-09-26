import os
import re
import textwrap
import urllib.parse

try:
    import pdfplumber
except ImportError:
    pdfplumber = None
import textwrap


TECHNICAL_SKILLS = [
    # Programming languages
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "PHP",
    "Ruby", "Go", "Rust", "Kotlin", "Swift", "R", "Dart", "Scala", "Bash",
    # Web
    "HTML", "CSS", "Bootstrap", "Tailwind CSS", "jQuery", "React", "Angular",
    "Vue", "Node.js", "Express.js", "Django", "Flask", "FastAPI",
    "Spring Boot", "REST API", "GraphQL", "JSON", "Microservices",
    "Web Development", "Frontend Development", "Backend Development",
    "Full Stack Development",
    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "Redis",
    "Database Management",
    # Tools, cloud and DevOps
    "Git", "GitHub", "Docker", "Kubernetes", "Linux", "AWS", "Azure",
    "Google Cloud", "Cloud Computing", "DevOps", "CI/CD", "Jenkins",
    "Postman", "Jira", "Agile", "Scrum",
    # CS fundamentals
    "Data Structures", "Algorithms", "OOP", "System Design", "Debugging",
    "Operating Systems", "Computer Networks", "Networking",
    # Data and AI
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "Generative AI", "Prompt Engineering", "NLP", "Computer Vision", "LLM",
    "Data Science", "Data Analysis", "Data Engineering", "Data Visualization",
    "Pandas", "NumPy", "Matplotlib", "Scikit-learn", "TensorFlow", "PyTorch",
    "Power BI", "Tableau", "Excel", "ETL", "Hadoop", "Spark", "Kafka",
    # Testing, security, mobile, design, others
    "Manual Testing", "Automation Testing", "Software Testing", "Selenium",
    "Cybersecurity", "Ethical Hacking", "Android Development",
    "iOS Development", "Flutter", "React Native", "UI/UX Design", "Figma",
    "Blockchain", "IoT", "Embedded Systems",
]

SOFT_SKILLS = [
    "Communication", "Teamwork", "Collaboration", "Leadership",
    "Problem Solving", "Critical Thinking", "Logical Thinking",
    "Analytical Skills", "Time Management", "Adaptability", "Flexibility",
    "Creativity", "Decision Making", "Conflict Resolution",
    "Emotional Intelligence", "Negotiation", "Presentation Skills",
    "Public Speaking", "Active Listening", "Interpersonal Skills",
    "Project Management", "Team Management", "Attention to Detail",
    "Work Ethic", "Multitasking", "Self Motivation", "Initiative",
    "Learning Agility", "Stress Management", "Organization",
    "Customer Service", "Mentoring", "Writing Skills", "Research",
    "Professionalism", "Patience", "Responsibility",
]

# Short forms people commonly type -> the proper skill name (lowercase)
ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "reactjs": "react",
    "react.js": "react",
    "node": "node.js",
    "nodejs": "node.js",
    "express": "express.js",
    "expressjs": "express.js",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "genai": "generative ai",
    "gen ai": "generative ai",
    "dsa": "data structures",
    "oops": "oop",
    "ui/ux": "ui/ux design",
    "ux": "ui/ux design",
    "sklearn": "scikit-learn",
    "gcp": "google cloud",
    "cpp": "c++",
    "problem-solving": "problem solving",
    "team work": "teamwork",
}

SKILL_LOOKUP = {
    skill.lower(): skill for skill in TECHNICAL_SKILLS + SOFT_SKILLS
}


def input_phone(prompt="Phone number: "):
    """Keep asking until the user enters a valid Indian mobile number.

    Rule (not shown to the user): exactly 10 digits, starting with 6, 7, 8 or 9.
    """

    while True:

        phone = input(prompt).strip()

        if re.fullmatch(r"[6-9][0-9]{9}", phone):
            return phone

        print("Invalid phone number. Please enter a valid mobile number.")


def input_email(prompt="Email: "):
    """Keep asking until the user enters a real-style Gmail address."""

    while True:

        email = input(prompt).strip().lower()

        if not email.endswith("@gmail.com"):
            print("Invalid email. Please enter a Gmail address (name@gmail.com).")
            continue

        username = email[: -len("@gmail.com")]

        # Gmail rules: 6-30 characters, only letters, numbers and dots,
        # dot cannot be first/last and two dots cannot be together
        if (
            re.fullmatch(r"[a-z0-9]+(\.[a-z0-9]+)*", username)
            and 6 <= len(username) <= 30
        ):
            return email

        print(
            "Invalid Gmail address. Username must be 6 to 30 characters "
            "(letters, numbers and dots only)."
        )


def input_skills(prompt="Skills: "):
    """Show the skills list, then keep asking until every skill entered is
    a real technical/soft skill.

    Returns the skills as one clean string, e.g. "Python, SQL, Teamwork".
    """

    show_skill_list()
    print("Enter skills from the list above, separated by commas.")

    while True:

        text = input(prompt).strip()

        if text == "?":
            show_skill_list()
            continue

        entered = [item.strip() for item in text.split(",") if item.strip()]

        if len(entered) == 0:
            print("Please enter at least one skill.")
            continue

        valid = []
        invalid = []

        for item in entered:

            key = item.lower()
            key = ALIASES.get(key, key)

            if key in SKILL_LOOKUP:

                skill = SKILL_LOOKUP[key]

                if skill not in valid:
                    valid.append(skill)

            else:
                invalid.append(item)

        if invalid:
            print("Not a valid skill:", ", ".join(invalid))
            print("Choose only from the technical and soft skills list (type ? to see it again).")
            continue

        return ", ".join(valid)


def clean_file_path(raw_path):
    """Turn a path copied from a browser/file-explorer link (which may
    look like file:///C:/Users/... or C:/Users/... with %20 for spaces)
    into a normal path Python can open."""

    path = raw_path.strip().strip('"').strip("'")

    if path.startswith("file:///"):
        path = path[len("file:///"):]
    elif path.startswith("file://"):
        path = path[len("file://"):]

    path = urllib.parse.unquote(path)

    # "/C:/Users/..." -> "C:/Users/..."
    if re.match(r"^/[A-Za-z]:", path):
        path = path[1:]

    return path


def extract_pdf_text(path):
    """Read all text from a PDF file and return it as one string."""

    text_parts = []

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def input_resume(prompt="Resume file path (PDF): "):
    """Keep asking until the user gives a real, readable PDF file.

    Returns (path, extracted_text). extracted_text is the actual words
    read from inside the PDF, not just the file name.
    """

    if pdfplumber is None:
        print(
            "\nThe 'pdfplumber' package is not installed, so the PDF "
            "cannot be read. Run: pip install pdfplumber"
        )
        path = input(prompt).strip().strip('"')
        return path, ""

    while True:

        path = clean_file_path(input(prompt))

        if not os.path.isfile(path):
            print(
                "File not found. Copy the path from File Explorer "
                "(Shift + Right-click the file -> Copy as path) and paste it here."
            )
            continue

        if not path.lower().endswith(".pdf"):
            print("Please provide a .pdf file.")
            continue

        try:
            text = extract_pdf_text(path)
        except Exception:
            print("Could not open this PDF. Try a different file.")
            continue

        if not text.strip():
            print(
                "No readable text found in this PDF "
                "(it may be a scanned image). Try another file."
            )
            continue

        return path, text


def show_skill_list():

    print("\nTechnical skills:")
    print(textwrap.fill(", ".join(TECHNICAL_SKILLS), width=78))

    print("\nSoft skills:")
    print(textwrap.fill(", ".join(SOFT_SKILLS), width=78))
    print()
def skill_match(candidate_skills, job_skills):
    """Compare a candidate's skills against a job's required skills.

    Returns (percent, matched, missing):
      percent - how much of the job's required skills the candidate has (0-100)
      matched - required skills the candidate already has
      missing - required skills the candidate is missing (the skill gap)
    """

    job_list = [s.strip() for s in job_skills.split(",") if s.strip()]

    candidate_lower = {
        s.strip().lower() for s in candidate_skills.split(",") if s.strip()
    }

    if len(job_list) == 0:
        return 0, [], []

    matched = [s for s in job_list if s.lower() in candidate_lower]
    missing = [s for s in job_list if s.lower() not in candidate_lower]

    percent = round(len(matched) / len(job_list) * 100)

    return percent, matched, missing


def print_skill_match(candidate_skills, job_skills):

    percent, matched, missing = skill_match(candidate_skills, job_skills)

    print("Skill Match:", str(percent) + "%")

    if matched:
        print("Matching skills:", ", ".join(matched))

    if missing:
        print("Skill gap (missing):", ", ".join(missing))
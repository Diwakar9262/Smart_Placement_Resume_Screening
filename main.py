from src.models.candidate import Candidate
from src.services.resume_service import ResumeService

def create_candidate():

    name = input("Enter Candidate Name : ")

    age = int(input("Enter Age : "))

    total_skills = int(input("How many skills? "))

    skills = []

    for i in range(total_skills):

        skill = input(f"Skill {i+1} : ")

        skills.append(skill)

    return Candidate(name, age, skills)


students = []

total = int(input("How many candidates? "))

for i in range(total):
    students.append(create_candidate())
service = ResumeService()
for student in students:
    student.display_info()
    print("Total Skills =", service.count_skills(student))
    print("Resume Score =", service.calculate_resume_score(student))
    print("Eligibility =", service.check_eligibility(student))
    print("-" * 30)

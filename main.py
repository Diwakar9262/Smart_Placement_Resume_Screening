from src.models.candidate import Candidate
from src.services.resume_service import ResumeService


student1 = Candidate(
    "Diwakar",
    19,
    ["python", "c++", "Git"]
)
student2 = Candidate(
    "Rahul",
    20,
    ["Python"]
)

student3 = Candidate(
    "Amit",
    21,
    ["Python", "Git", "SQL", "Excel"]
)

students = [
    student1,
    student2,
    student3
]

service = ResumeService()

for student in students:
    student.display_info()
    print("Total Skills =", service.count_skills(student))
    print("Resume Score =", service.calculate_resume_score(student))
    print("Eligibility =", service.check_eligibility(student))
    print("-" * 30)

from src.models.candidate import Candidate
from src.services.resume_service import ResumeService


student1 = Candidate(
    "Diwakar",
    19,
    ["python", "c++", "Git"]
)
student1.display_info()
print("Candidate Score =", student1.calculate_score())

service = ResumeService()
print("Total skills = ", service.count_skills(student1))
print("Total Resume Score = ",service.calculate_resume_score(student1))
print("Eligibility = ",service.check_eligibility(student1))
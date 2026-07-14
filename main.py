from src.models.candidate import Candidate
from src.services.resume_service import ResumeService
from src.utils.file_handler import save_candidates

service = ResumeService()
students = []
def create_candidate():

    name = input("Enter Candidate Name : ")

    age = int(input("Enter Age : "))

    total_skills = int(input("How many skills? "))

    skills = []

    for i in range(total_skills):

        skill = input(f"Skill {i+1} : ")

        skills.append(skill)

    return Candidate(name, age, skills)



def add_candidate():

    student = create_candidate()
    students.append(student)
    save_candidates(students)
    print("Candidate Added Successfully.")

def show_candidates():
    if len(students) == 0:
        print("No Candidates Found!")
        return
    for student in students:
        student.display_info()
        print("Total Skills =", service.count_skills(student))
        print("Resume Score =", service.calculate_resume_score(student))
        print("Eligibility =", service.check_eligibility(student))
        print("-" * 30)

while True:

    print("\n========== Resume Screening ==========")
    print("1. Add Candidate")
    print("2. Show Candidates")
    print("3. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":
        add_candidate()

    elif choice == "2":
        show_candidates()

    elif choice == "3":
        print("Thank You")
        break

    else:
        print("Invalid Choice")

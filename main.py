from src.models.candidate import Candidate
from src.services.resume_service import ResumeService
from src.utils.file_handler import save_candidates, load_candidates
from src.utils.csv_handler import export_to_csv
from src.services.ml_service import MLService

service = ResumeService()
ml_service = MLService()
students = load_candidates()
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
        print("AI Resume Score =", ml_service.predict_score(student))
        print("Skill Match =", service.calculate_skill_match(student), "%")
        print("Missing Skills =", service.missing_skills(student))
        recommendations = service.recommend_skills(student)

        if len(recommendations) == 0:
            print("Recommendations = None")
        else:
            print("Recommendations =")
            for item in recommendations:
                print("-", item)
        print("Eligibility =", service.check_eligibility(student))
        print("-" * 30)
def show_ranking():

    ranked_students = sorted(
        students,
        key=lambda student: ml_service.predict_score(student),
        reverse=True
    )

    print("\n========== Candidate Ranking ==========")

    rank = 1

    for student in ranked_students:

        print(f"{rank}. {student.name}")
        print("AI Resume Score =", ml_service.predict_score(student))
        print("-" * 30)

        rank += 1
def search_candidate():
    name = input("Enter Candidate Name : ")
    for student in students:
        if student.name.lower() == name.lower():
            student.display_info()

            print("Total Skills =", service.count_skills(student))

            print("Resume Score =", service.calculate_resume_score(student))

            print("Eligibility =", service.check_eligibility(student))

            return

    print("Candidate Not Found!")
def delete_candidate():
    name = input("Enter Candidate Name : ")
    for student in students:
        if student.name.lower() == name.lower():
            students.remove(student)
            save_candidates(students)
            print("Candidate Deleted Successfully!")
            return
    print("Candidate Not Found!")
def update_candidate():
    name = input("Enter Candidate Name : ")
    for student in students:
        if student.name.lower() == name.lower():
            student.age = int(input("Enter New Age : "))
            total_skills = int(input("How many skills? "))
            skills = []
            for i in range(total_skills):

                skill = input(f"Skill {i+1} : ")
                skills.append(skill)
            student.skills = skills
            save_candidates(students)
            print("Candidate Updated Successfully!")
            return
    print("Candidate Not Found!")
while True:

    print("\n========== Resume Screening ==========")
    print("1. Add Candidate")
    print("2. Show Candidates")
    print("3. Search Candidate")
    print("4. Delete Candidate")
    print("5. Update Candidate")
    print("6. Export to CSV")
    print("7. Show Ranking")
    print("8. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":
        add_candidate()

    elif choice == "2":
        show_candidates()

    elif choice == "3":
        search_candidate()

    elif choice == "4":
        delete_candidate()

    elif choice == "5":
        update_candidate()
        
    elif choice == "6":
        export_to_csv(students)

    elif choice == "7":
        show_ranking()

    elif choice == "8":
        print("Thank You")
        break

    else:
        print("Invalid Choice")

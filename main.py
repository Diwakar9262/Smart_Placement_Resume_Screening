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
def dashboard_summary():

    if len(students) == 0:
        print("No Candidates Found!")
        return
    total = len(students)
    eligible = 0

    for student in students:

        if service.check_eligibility(student) == "Eligible":
            eligible += 1

        not_eligible = total - eligible
    total_ai = 0

    for student in students:

        total_ai += ml_service.predict_score(student)

    average_ai = total_ai / total
    highest = max(
        students,
        key=lambda student: ml_service.predict_score(student)
    )

    lowest = min(
        students,
        key=lambda student: ml_service.predict_score(student)
    )
    total_match = 0

    for student in students:

        total_match += service.calculate_skill_match(student)

    average_match = total_match / total
    print("\n========== Dashboard Summary ==========")

    print("Total Candidates :", total)

    print("Eligible Candidates :", eligible)

    print("Not Eligible :", not_eligible)

    print()

    print("Average AI Score :", round(average_ai, 2))

    print()

    print("Highest AI Score :")

    print(highest.name, "-", round(ml_service.predict_score(highest), 2))

    print()

    print("Lowest AI Score :")

    print(lowest.name, "-", round(ml_service.predict_score(lowest), 2))

    print()

    print("Average Skill Match :", round(average_match, 2), "%")
def filter_candidates():

    while True:

        print("\n========== Candidate Filters ==========")
        print("1. Show Eligible Candidates")
        print("2. Show AI Score > 80")
        print("3. Show Skill Match >= 75%")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":

            print("\nEligible Candidates\n")

            for student in students:

                if service.check_eligibility(student) == "Eligible":

                    print(student.name)
                    print("AI Score =", round(ml_service.predict_score(student), 2))
                    print("-" * 30)

        elif choice == "2":

            print("\nCandidates with AI Score > 80\n")

            for student in students:

                score = ml_service.predict_score(student)

                if score > 80:

                    print(student.name)
                    print("AI Score =", round(score, 2))
                    print("-" * 30)

        elif choice == "3":

            print("\nCandidates with Skill Match >= 75%\n")

            for student in students:

                match = service.calculate_skill_match(student)

                if match >= 75:

                    print(student.name)
                    print("Skill Match =", match, "%")
                    print("-" * 30)

        elif choice == "4":
            break

        else:
            print("Invalid Choice")
def search_by_skill():

    skill_name = input("Enter Skill : ").lower()

    found = False

    print("\nCandidates with", skill_name.upper(), "Skill\n")

    for student in students:

        for skill in student.skills:

            if skill.lower() == skill_name:

                print(student.name)
                print("AI Score =", round(ml_service.predict_score(student), 2))
                print("Skills =", student.skills)
                print("-" * 30)

                found = True

                break

    if not found:
        print("No Candidate Found with this skill.")
def search_multiple_skills():

    skills = input("Enter Skills (comma separated): ").lower().split(",")

    skills = [skill.strip() for skill in skills]

    found = False

    print("\nCandidates Matching All Skills\n")
    for student in students:

        student_skills = [skill.lower() for skill in student.skills]

        if all(skill in student_skills for skill in skills):

            print(student.name)
            print("AI Score =", round(ml_service.predict_score(student), 2))
            print("Skills =", student.skills)
            print("-" * 30)

            found = True
    if not found:

        print("No Candidate Found.")
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
    print("8. Dashboard Summary")
    print("9. Candidate Filters")
    print("10. Search by Skill")
    print("11. Search by Multiple Skills")
    print("12. Exit")

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
        dashboard_summary()
    elif choice == "9":
        filter_candidates()
    elif choice == "10":
        search_by_skill()
    elif choice == "11":
        search_multiple_skills()
    elif choice == "12":
        print("Thank You")
        break

    else:
        print("Invalid Choice")

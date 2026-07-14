import csv



def export_to_csv(candidate_list):
    with open("data/candidates.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Age", "Skills"])
        for candidate in candidate_list:
            writer.writerow([
                candidate.name,
                candidate.age,
                ", ".join(candidate.skills)
            ])
    print("Candidates exported successfully!")
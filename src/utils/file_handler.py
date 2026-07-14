import json
from src.models.candidate import Candidate


def save_candidates(candidate_list):

    data = []

    for candidate in candidate_list:
        data.append(candidate.to_dict())

    with open("data/candidates.json", "w") as file:
        json.dump(data, file, indent=4)
def load_candidates():

    with open("data/candidates.json", "r") as file:

        data = json.load(file)

    students = []

    for item in data:

        candidate = Candidate(
            item["name"],
            item["age"],
            item["skills"]
        )

        students.append(candidate)

    return students
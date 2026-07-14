import json

def save_candidates(candidate_list):

    data = []

    for candidate in candidate_list:
        data.append(candidate.to_dict())

    with open("data/candidates.json", "w") as file:
        json.dump(data, file, indent=4)
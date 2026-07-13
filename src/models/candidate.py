class Candidate:

    def __init__(self , name, age, skills):
        self.name = name
        self.age = age
        self.skills = skills

    def display_info(self):
        print("Candidate Name = ", self.name)
        print("Age = ", self.age)
        print("Skills = ", self.skills)

    def calculate_score(self):
        score = len(self.skills) *10
        return score

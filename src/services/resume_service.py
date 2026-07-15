required_skills = [
    "python",
    "sql",
    "git",
    "c++"
]
class ResumeService:
    def count_skills(self, candidate):
        return len(candidate.skills)

    def calculate_resume_score(self, candidate):
        score = 0

        for skill in candidate.skills:
            if skill.lower() == "python":
                score += 40
            elif skill.lower() == "git":
                score += 10
            elif skill.lower() == "c++":
                score += 15
            elif skill.lower() == "c":
                score += 20            
        return score 
    def check_eligibility(self, candidate):
        score = self.calculate_resume_score(candidate)

        if score >= 60:
            return "Eligible" 
        return "Not Eligible"
    def calculate_skill_match(self, candidate):

        matched = 0

        for skill in candidate.skills:

            if skill.lower() in required_skills:
                matched += 1

        percentage = (matched / len(required_skills)) * 100

        return round(percentage, 2)
    def missing_skills(self, candidate):

        missing = []

        for skill in required_skills:

            if skill not in [s.lower() for s in candidate.skills]:

                missing.append(skill)

        return missing
    


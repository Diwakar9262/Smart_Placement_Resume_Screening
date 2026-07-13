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

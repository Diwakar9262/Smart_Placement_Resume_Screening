import joblib
import pandas as pd

class MLService:

    def __init__(self):
        self.model = joblib.load("resume_model.pkl")
    def predict_score(self, candidate):

        data = pd.DataFrame({
            "Skills": [len(candidate.skills)],
            "Age": [candidate.age]
        })

        prediction = self.model.predict(data)

        return round(prediction[0], 2)
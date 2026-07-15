import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/resume_dataset.csv")

X = df[["Skills", "Age"]]

y = df["ResumeScore"]

model = LinearRegression()

model.fit(X, y)

new_candidate = pd.DataFrame({
    "Skills": [5],
    "Age": [22]
})

prediction = model.predict(new_candidate)

print("Predicted Resume Score =", prediction)
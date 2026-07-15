import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/resume_dataset.csv")

X = df[["Skills", "Age"]]

y = df["ResumeScore"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = LinearRegression()

model.fit(X_train, y_train)

joblib.dump(model, "resume_model.pkl")

y_pred = model.predict(X_test)

print("Predictions:")
print(y_pred)

mae = mean_absolute_error(y_test, y_pred)

print("Mean Absolute Error =", mae)
loaded_model = joblib.load("resume_model.pkl")

new_candidate = pd.DataFrame({
    "Skills": [5],
    "Age": [22]
})

prediction = model.predict(new_candidate)

print("Predicted Resume Score =", prediction)
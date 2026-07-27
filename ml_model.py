import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = {
    "attendance": [95,90,85,80,75,70,65,60,55,50],
    "tasks": [30,28,25,22,20,18,15,12,10,8],
    "rating": [5,5,4,4,3,3,2,2,1,1],
    "performance":[
        "Excellent",
        "Excellent",
        "Good",
        "Good",
        "Average",
        "Average",
        "Average",
        "Poor",
        "Poor",
        "Poor"
    ]
}

df = pd.DataFrame(data)

X = df[["attendance","tasks","rating"]]
y = df["performance"]

model = DecisionTreeClassifier(random_state=42)
model.fit(X,y)

def predict_performance(attendance,tasks,rating):
    result = model.predict([[attendance,tasks,rating]])
    return result[0]
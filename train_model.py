import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import kagglehub
import os

path = kagglehub.dataset_download(
    "shriyashjagtap/indian-personal-finance-and-spending-habits"
)

csv_file = os.path.join(path, "data.csv")
df = pd.read_csv(csv_file)

features = [
    "Income","Age","Dependents","Rent","Loan_Repayment",
    "Insurance","Groceries","Transport","Eating_Out",
    "Entertainment","Utilities","Healthcare","Education","Miscellaneous"
]

target = "Desired_Savings"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
score = r2_score(y_test, pred)

pickle.dump(model, open("savings_model.pkl", "wb"))

print("Model Training Completed")
print(f"R2 Score: {score:.4f}")
print("Saved as savings_model.pkl")
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict, List, Annotated, Optional
from pydantic import BaseModel, Field
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, OrdinalEncoder
import pandas as pd
import pickle

app = FastAPI()

with open("model_ML.pkl","rb") as f:
    model = pickle.load(f)

print(model.feature_names_in_)

class HeartDisease(BaseModel):
    Age :  int = Field(ge=0, le=70)
    Gender : str
    bp : Annotated[float, Field(...,description="Blood Pressure")]
    cholesterol : Annotated[float, Field(...,description="Cholesterol Level")]
    exercise_habit : Annotated[str, Field(...,description="Exercise Habits", 
                                          examples=["High", "Medium", "Low"])]
    smokes : Annotated[str, Field(...,description="Smoking Status")]
    family_hrt_ds : Annotated[str, Field(description="Previous Family heart disease status")]
    diabetes : Annotated[str, Field(description="diabetes status")]
    bmi : float
    stress_level : Annotated[str, Field(description="Level of stress")]
    sugar_consumption : str

@app.get("/")
def hello():
    return {"message": "hello man!!!"}

@app.post("/predict")
def predict(data: HeartDisease):
    data_dict = data.model_dump()

    # Map Pydantic field names to model column names
    rename_map = {
        "bp": "Blood Pressure",
        "cholesterol": "Cholesterol Level",
        "exercise_habit": "Exercise Habits",
        "smokes": "Smoking",
        "family_hrt_ds": "Family Heart Disease",
        "diabetes": "Diabetes",
        "bmi": "BMI",
        "stress_level": "Stress Level",
        "sugar_consumption": "Sugar Consumption",
        "Age": "Age",
        "Gender": "Gender"
    }

    # Convert into the correct format for model
    formatted = {rename_map[k]: v for k, v in data_dict.items()}
    input_df = pd.DataFrame([formatted])

    # Make prediction
    prediction = model.predict(input_df)[0]
    return {"prediction": str(prediction)}


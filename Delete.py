from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, AnyUrl, EmailStr, computed_field
from typing import Annotated, Optional, Dict, List, Literal
import json

# Literal is used to provide options to the user, Like can be used in gender selection

app = FastAPI()

class Patients(BaseModel):
    id : Annotated[str, Field(..., description='id of the patient', example='P001')]
    name : Annotated[str, Field(...,description='name of the patient', example='Kishan')]
    city : Annotated[str, Field(..., description='name of city the patient belongs to')]
    age : Annotated[int, Field(..., gt=0, lt=120)]
    gender : Annotated[Literal['Male','Female','Others'], Field(..., description='Gender')]
    height : Annotated[float, Field(..., le=7, ge=1, description='Height of the patient in feet')]
    weight : Annotated[float, Field(..., gt=0, description='weight of patient')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2) ,2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if (self.bmi < 18.5):
            return "Underweight"
        elif(self.bmi < 30):
            return "Normal"
        elif(self.bmi > 30):
            return "Overweight"

# As the previous pydantic model cannot be used in updating, because in the previous model,
# all the fields are set to be "required" !
class Patient_Update(BaseModel):
    # id : Annotated[str, Field(..., description='id of the patient', example='P001')]
    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender : Annotated[Optional[Literal['Male','Female','Others']], Field(default=None)]
    height : Annotated[Optional[float], Field(le=7, ge=1, default=None)]
    weight : Annotated[Optional[float], Field(gt=0, default=None)]

        
def load_data():
    with open('datas.json') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('datas.json', 'w') as f:
        json.dump(data, f)
    

@app.get("/")
def hello():
    return {"message": "Hello world"}

@app.get("/about")
def about():
    return {"message": "Kishan is making a new web page that is hosted in this machine only"}

@app.get("/contact")
def kishan():
    return {"message" : "Contact information : 9863139834 "}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{pat_ID}")
def patient(pat_ID:str = Path(..., description='ID of the patient', example='1')):
    id = "P00" + (pat_ID)
    data = load_data()
    
    if (id in data):
        return data[id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get("/sort")
def sort_params(sort_by:str=Query(..., description="sort on the basis of given param"), 
                ordr:str=Query(..., description="order of sorting")):
    sort = ["height", "weight", "age"]
    order = ['inc', 'dec']
    if (sort_by not in sort):
        raise HTTPException(status_code=400, detail=f'chose from {sort}')
    if (ordr not in order):
        raise HTTPException(status_code=400, detail=f'chose from {ordr}')
    
    data = load_data()  
    sort_order = True if ordr=='dec' else False
    
    sorteddata = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)
    return sorteddata

@app.post("/create")
def create_patient(patient : Patients):
    # Load all the existing data
    data = load_data()
    # Check if the given patient already exists or not
    if (patient.id in data):
        raise HTTPException(status_code=400, detail='Patient already exists !')
    # Add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # Save the data
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_UPDATE:Patient_Update):
    data = load_data()
    
    if (patient_id not in data):
        raise HTTPException(status_code=400, detail='Patient not found !')
    
    existing_patient_info = data[patient_id]
    Updated_patient_info = patient_UPDATE.model_dump(exclude_unset=True)
    
    for key, value in Updated_patient_info.items():
        existing_patient_info[key] = value
        
    # As soon as we update our weights, bmi and verdict also changes 
    # To update these values, we have to create a new pydantic object 
    
    # existing_patient_info -> pydantic object (Patients) -> bmi + verdict (new values)-> change to
    existing_patient_info['id'] = patient_id
    patient_pydantic = Patients(**existing_patient_info)
    # dict -> update the values
    existing_patient_info = patient_pydantic.model_dump(exclude='id')    
    
    data[patient_id] = existing_patient_info
    
    save_data(data)
    
    return JSONResponse(status_code=200, content='Patient updated successfully')

@app.delete('/delete/{pat_id}')
def delete_patient(pat_id:str):
    data = load_data()
    
    if (pat_id not in data):
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[pat_id]
    save_data(data)
    
    return JSONResponse(status_code=200,content='Patient deleted successfully')
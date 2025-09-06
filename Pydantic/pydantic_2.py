from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

# "Annotated" and "Field" is used to create metadata in the docs of the API 
class Patients(BaseModel):
    name : Annotated[str, Field(max_length=50, title='Name of Patient',description="Give the name of the patient in less than 50 chars", examples=['Nitish', 'Kishan'])]
    age : int = Field(ge=0, le=60)
    email:EmailStr
    pat_url : AnyUrl
    weight : Annotated[Optional[float], Field(default=60, description="defalut value 60, give the weight of the patient")]
    # Annotated can also be used to make parameters Optional by setting a defalut value
    married : Optional[bool] = None
    contact_details : Dict[str, str]
    allergies : List[str]

def pat_1(patiens: Patients):
    print(patiens.name)
    print(patiens.age)
    print("added 111")
    
def update(patients: Patients):
    print(patients.name) 
    print(patients.age)
    print("Updated")

pate = {"name":"Kishan", "age":50, "email":"bhadrakishan717@gmail.com","pat_url":"https.kisan.com", "married":"", "phone":"9863139834", "allergies":["pollen","egg"], "contact_details":"+91 9863139834"}

patients = Patients(**pate)

pat_1(patients)



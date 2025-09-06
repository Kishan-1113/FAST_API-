from pydantic import BaseModel

class Patients(BaseModel):
    name : str
    age : int
    weight = int

def pat_1(patiens: Patients):
    print(patiens.name)
    print(patiens.age)
    print("added 111")
    
def update(patients: Patients):
    print(patients.name) 
    print(patients.age)
    print("Updated")

pate = {"name":"Kishan", "age": 20}

patients = Patients(**pate)

pat_1(patients)



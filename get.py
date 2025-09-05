from fastapi import FastAPI, Path, HTTPException, Query
import json

app1 = FastAPI()

def load_data():
    with open("datas.json", "r") as f:
        data = json.load(f)
    return data    
        

@app1.get("/")
def hello():
    return {"message": "Hello world"}

@app1.get("/about")
def about():
    return {"message": "Kishan is making a new web page that is hosted in this machine only"}

@app1.get("/contact")
def kishan():
    return {"message" : "Contact information : 9863139834 "}

@app1.get("/view")
def view():
    data = load_data()
    return data

@app1.get("/patient/{pat_ID}")
def patient(pat_ID:str = Path(..., description='ID of the patient', example='1')):
    id = "P00" + (pat_ID)
    data = load_data()
    
    if (id in data):
        return data[id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app1.get("/sort")
def sort_params(sort_by:str=Query(..., description="sort on the basis of given param"), 
                ordr:str=Query(..., description="order of sorting")):
    sort = ["height", "weight", "age"]
    order = ['inc', 'dec']
    if (sort_by not in sort):
        raise HTTPException(status_code=400, detail='chose from {sort}')
    if (ordr not in order):
        raise HTTPException(status_code=400, detail='chose from {ordr}')
    
    data = load_data()
    sort_order = True if ordr=='dec' else False
    
    sorteddata = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)
    return sorteddata
    
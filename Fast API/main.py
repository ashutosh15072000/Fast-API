from fastapi import FastAPI,Path,HTTPException,Query
import json
from Pydantic import BaseModel,Field,Computed_field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse 
app=FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description="Id of the patient",examples=["p001"])]
    
    name: Annotated[str,Field(...,description="Name of the patient")]
    
    city: Annotated[str,Field(...,description="City where the patient is living ")]

    age: Annotated[int,Field(...,gt=0,lt=120,description="Age of the Patient")]

    gender: Annotated[Literal['male',"female","others"],Field(...,description="Gender of the Patient")]
    
    height: Annotated[float,Field(...,gt=0,description="Height of the patient in mtrs")]

    weight: Annotated[float,Field(...,gt=0,description="Weight of the patient in kgs")]

    @Computed_field
    @property
    def bmi(self) ->float:
        return round(self.weight/(self.height**2),2)

    @Computed_field
    @property
    def verdict(self) -> str:
        if self.bmi<18.5:
            return "UnderWeight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Normal"
        else:
            return "Obese"
        
def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open("patient.json","w") as f:
        json.dump(data,f,indent=4)

@app.get("/")
def hello():
    return {"message": "Patient Mangement System API "}

@app.get("/about")
def about():
    return {"message": "A Fully Functional API to Manage your patient records"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description="ID of the patient in the DB",example="P001")):
    # Load all the patient
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="Sort on the basis of height ,weight and Bmi"),order: str = Query("asc",description="Sort in Asc or Desc Order")):
    valid_fields=['height',"weight","bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Invalid field select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f"Invalid order select from {['asc','desc']}")
    data=load_data()
    sort_order= True if order=='desc' else False
    sorted_data = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    ## Load existinf data
    data = load_data()

    ## Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")

    ## new patient and to the database
    data[patient.id]=patient.model_dump(exclude=['id'])

    ## Save into the json file
    save_data(data)

    ## 

    return JSONResponse(status_code="201",content={"message":"Patient created successfully"})

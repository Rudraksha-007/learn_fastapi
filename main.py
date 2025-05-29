from fastapi import FastAPI,Path,HTTPException,Query
import json
app=FastAPI()


def load_data():
    with open("patient.json",'r')as file:
        data=json.load(file)
    return data

@app.get("/")
def index():
    return"Hello"
@app.get("/about")
def about():
    return {"message":"This API is to manage your patient records"}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(...,description="Enter the ID of the patient",example="54")):
    # load all the data
    data=load_data()
    for dic in data:
        if int(patient_id) == dic["id"]:
            return dic
    raise HTTPException(status_code=404,detail="Patient Not found :-C")

@app.get("/sort")
def sort_patient(sort_by:str=Query(...,description="Sort on the basis of age,height"),
                 order:str= Query('asc',description="Sort in which order")):
    valid_fields=("height","age")
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Invalid field select form {valid_fields}")
    if order not in ('asc','dsc'):
        raise HTTPException(status_code=400,detail=f"Invalid sort by select form asc or dsc")
    data=load_data()
    s_data=sorted(data,key=lambda dic : dic[sort_by],reverse=True if order=='dsc' else False)
    return s_data
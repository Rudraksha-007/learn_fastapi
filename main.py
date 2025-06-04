from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Path,HTTPException,Query
import json
app=FastAPI()

# class Patient(BaseModel):
#     name:Annotated[str,Field(...,max_length=50,title="Name of the patient not a PK in the DB",description="used to describe the non PK attribute of name",examples=["Nitish"])]
#     age:int
#     linkedin_Url:AnyUrl
#     email:EmailStr
#     married:Annotated[bool, Field(default=False,description="is the patient married or not?")]
#     weight:Annotated[float,Field(strict=True,gt=0,le=120)]
#     allergies:Annotated[Optional[List[str]],Field(default=None,max_length=16)]
#     contact_detail:Dict[str,str]

class Patient2(BaseModel):
    id:int
    name:str
    age:int
    # linkedin_Url:Optional[AnyUrl]
    # email:EmailStr
    # married:bool
    weight:float
    height:float
    # allergies:List[str]
    # contact_detail:Dict[str,str]
    
    @computed_field
    @property
    def BMI(self)->float:
        # this makes a attribute called "BMI" in the pydantic model
        if self.height==0:
            raise HTTPException(status_code=400,detail="tohar mai ke chodo 0 height hola re !?")
        return round((self.weight/self.height**2),2)
    # @field_validator('email')
    # @classmethod
    # def valid(cls,value):
    #     valid_domains=('hdfc','icici')
    #     domain_name=value.split('@')[-1]
    #     if domain_name not in valid_domains:
    #         raise ValueError("cannot treat this patient")
    #     else:
    #         return value
    # this mode specifies when does field validator gets the value (before or after type coreation)
    @field_validator('name',mode="after")
    @classmethod
    def transform_name(cls,name):
        return name.upper()
    
    # @model_validator(mode="after")
    # def validate_emergency_Contact(cls,model):
    #     if model.age>=60 and "emergencyph" not in model.contact_detail.keys():
    #         raise ValueError("Patient older than 60 must have a emergency ph")
    #     else:
    #         return model
    @computed_field(return_type=str)
    @property
    def verdict(self):
        if self.BMI<18.5:
            return "UnderWeight"
        elif self.BMI<30:
            return "Normal"
        else:
            return "Obese"

class patientUpdate(BaseModel):
    name:Annotated[str,Field(...,max_length=50,title="Name of the patient not a PK in the DB",description="used to describe the non PK attribute of name",examples=["Nitish"])]
    age:int
    linkedin_Url:AnyUrl
    email:EmailStr
    married:Annotated[bool, Field(default=False,description="is the patient married or not?")]
    weight:Annotated[float,Field(strict=True,gt=0,le=120)]

def load_data():
    with open("patient.json",'r')as file:
        data=json.load(file)
    return data

def save_data(data):
    with open("patient.json",'w')as file:
        json.dump(data,file)
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

@app.post("/create")
def create_Patient(patient:Patient2):
    # load existing data
    data=load_data()
    # check for duplicates
    for dict in data:
        if dict["id"]==patient.id:
            raise HTTPException(status_code=400,detail="Patient already exist")
    # else add the new patient
    data[patient.id]=patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=201,content={"Message":"Patient admitted."})

@app.put("/edit/{patient_id}")
def update(patient_id:str , reqbody:patientUpdate):
    data=load_data()
    patient_data={}
    for dict in data:
        if dict["id"]==patient_id:
            patient_id=dict
    if len(patient_data)==0:
        raise HTTPException(status_code=400,detail="Patient not found ")
    # only contains relevent update info nothing else :
    update_info=reqbody.model_dump(exclude_unset=True)
    for key,value in update_info.items():
        patient_data[key]=value
    patient_data["id"]=patient_id
    p1=Patient2(**patient_data)
    patient_data=p1.model_dump(exclude={"id"})
    for dict in data:
        if dict["id"]==patient_id:
            dict=patient_data
    save_data(data)
    return JSONResponse(status_code=200,content={"message":"patient updated."})
    return JSONResponse(status_code=200,content={"message":"patient updated."})

@app.delete("/delete/{patient_id}")
def delPatient(patient_id:str):
    data=load_data()
    for dict in data:
        if dict["id"]==patient_id:
            del dict
            break
    save_data(data)
    return JSONResponse(status_code=200,content={"message":"patient deleted."})
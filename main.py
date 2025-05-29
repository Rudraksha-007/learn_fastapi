from fastapi import FastAPI
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
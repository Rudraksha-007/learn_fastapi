from faker import Faker
from main import load_data
import json
import random

def generate_height_cm(min_cm=150, max_cm=200):
    return round(random.uniform(min_cm, max_cm), 1) 
fake=Faker()
patients=[]
for i in range(100):
    patients.append({
        "id":i,
        "name":fake.name(),
        "height":generate_height_cm(),
        "age":random.randint(15,90),        
        "phone":fake.phone_number(),
        "address":fake.address(),
        "verdict":fake.word(ext_word_list=["flu", "covid", "cold"])

    })

with open("patient.json","w") as file:
    json.dump(patients,file,indent=2)
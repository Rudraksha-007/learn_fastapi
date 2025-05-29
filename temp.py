from faker import Faker
import json
import random
def generate_height_cm(min_cm=150, max_cm=200):
    return round(random.uniform(min_cm, max_cm), 1) 
fake=Faker()
patients=[]
for _ in range(100):
    patients.append({
        "name":fake.name(),
        "height":generate_height_cm(),
        "phone":fake.phone_number(),
        "address":fake.address(),
        "verdict":fake.word(ext_word_list=["flu", "covid", "cold"])
    })
with open("patient.json","w") as file:
    json.dump(patients,file,indent=2)
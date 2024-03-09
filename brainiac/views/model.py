import random
from flask import current_app

celery = current_app.celery

@celery.task(name="process_case")
def process_case(patient_data, case_no, img_urls):
    
    #pass the images into the model here
    prediction = "random prediction"
    accuracy = random.choice([25, 50, 75])
    
    #update the patient data
    case_name = "case" + str(case_no)
    current_app.db.patients.update_one(
        {"user_id": patient_data["user_id"]},
        {
            "$set": {"case_details." + case_name + ".status": "Completed",
                     "case_details." + case_name + ".prediction": prediction,
                     "case_details." + case_name + ".accuracy": accuracy
                     }
        })
    
    #Assign the case to a doctor
    doctor_id = random.choice([14,16])

    #update the doctor data
    current_app.db.doctors.update_one(
        {"user_id": doctor_id},
        {
            "$push": {"cases": [patient_data["user_id"], case_no]}
        }
    )
import random
from flask import current_app

celery = current_app.celery

@celery.task(name="process_case")
def process_case(patient_data, case_name, img_urls):
    
    #pass the images into the model here
    prediction = "random prediction"
    accuracy = random.choice([25, 50, 75])
    
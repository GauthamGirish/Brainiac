import random
from flask import current_app
from . import model_utils
from collections import Counter

model = model_utils.load_model('tumor_classifier_model.pth')


def process_case(patient_data, case_no, img_urls):
    # Perform prediction
    predictions = []
    accuracies = []

    for img_url in img_urls:
        image = model_utils.preprocess_img(img_url)
        predicted_class, confidence = model_utils.predict(model, image)
        predictions.append(predicted_class)
        accuracies.append(confidence)

    labels = ['glioma', 'meningioma', 'notumor', 'pituitary']
    # Calculate overall prediction and accuracy
    pred_idx = Counter(predictions).most_common(1)[0][0]

    # pass the images into the model here
    prediction = labels[pred_idx]
    accuracy = sum(accuracies) / len(accuracies)

    # Assign the case to a doctor
    # doctor_id = random.choice([14, 15])
    doctor_id = 23  # predoc

    # update the patient data
    case_name = "case" + str(case_no)
    current_app.db.patients.update_one(
        {"user_id": patient_data["user_id"]},
        {
            "$set": {"case_details." + case_name + ".status": "Under Review",
                     "case_details." + case_name + ".prediction": prediction,
                     "case_details." + case_name + ".accuracy": accuracy,
                     "case_details." + case_name + ".doctor_id": doctor_id
                     }
        })

    # update the doctor data
    current_app.db.doctors.update_one(
        {"user_id": doctor_id},
        {
            "$push": {"cases": [patient_data["user_id"], case_no]}
        }
    )


# def process_case(patient_data, case_no, img_urls):

#     # pass the images into the model here
#     prediction = "random prediction"
#     accuracy = random.choice([25, 50, 75])

#     # Assign the case to a doctor
#     doctor_id = random.choice([14, 15])

#     # update the patient data
#     case_name = "case" + str(case_no)
#     current_app.db.patients.update_one(
#         {"user_id": patient_data["user_id"]},
#         {
#             "$set": {"case_details." + case_name + ".status": "Under Review",
#                      "case_details." + case_name + ".prediction": prediction,
#                      "case_details." + case_name + ".accuracy": accuracy,
#                      "case_details." + case_name + ".doctor_id": doctor_id
#                      }
#         })

#     # update the doctor data
#     current_app.db.doctors.update_one(
#         {"user_id": doctor_id},
#         {
#             "$push": {"cases": [patient_data["user_id"], case_no]}
#         }
#     )

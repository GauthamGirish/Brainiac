import random
from flask import current_app
from model_utils import load_model, preprocess_img, predict
from collections import Counter

# Load the model
model_path = r'C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[C] CSE301\[0] Brainiac Repo\tumor_classifier_model.pth'
model = load_model(model_path)

# Define absolute paths to the test images
test_img_urls = [
    r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[C] CSE301\[0] Brainiac Repo\brainiac\static\images\Te-pi_0010.jpg",
    r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[C] CSE301\[0] Brainiac Repo\brainiac\static\images\Te-pi_0011.jpg",
    r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[C] CSE301\[0] Brainiac Repo\brainiac\static\images\Te-pi_0012.jpg",
    r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[C] CSE301\[0] Brainiac Repo\brainiac\static\images\Te-pi_0013.jpg",
    r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[C] CSE301\[0] Brainiac Repo\brainiac\static\images\Te-pi_0014.jpg"
]

# Perform prediction
predictions = []
accuracies = []

for img_url in test_img_urls:
    image = preprocess_img(img_url)
    predicted_class, confidence = predict(model, image)
    predictions.append(predicted_class)
    accuracies.append(confidence)

labels = ['glioma', 'meningioma', 'notumor', 'pituitary']
# Calculate overall prediction and accuracy
most_common_label = Counter(predictions).most_common(1)[0][0]
accuracy = sum(accuracies) / len(accuracies)


print("All Predictions:", predictions)
print("Most common predicted class label:", labels[most_common_label])
print("Average Accuracy:", accuracy)
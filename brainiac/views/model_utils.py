import torch
import torch.nn as nn
import torchvision.transforms as transforms
import requests
from PIL import Image
from io import BytesIO


# Data augmentation
img_transform = trans_pipeline = transforms.Compose([
    transforms.Resize((224, 224)),         # Resize images to 224x224 pixels
    transforms.ToTensor(),                  # Convert images to PyTorch tensors
    transforms.Normalize(                   # Normalize pixel values
        mean=[0.485, 0.456, 0.406],         # Mean values for each color channel
        std=[0.229, 0.224, 0.225]           # Standard deviation values for each color channel
    )
])


def load_model(path):
    model = nn.Sequential(
        nn.Conv2d(3, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2, 2),
        nn.Conv2d(16, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2, 2),
        nn.Flatten(),
        nn.Linear(32 * 56 * 56, 128),  # Adjust input size acc to image size
        nn.ReLU(),
        nn.Linear(128, 4)
    )

    # Load the trained model state dict
    model.load_state_dict(torch.load(path,  map_location=torch.device('cpu')))
    model.eval()  # Set the model to evaluation mode
    return model


def preprocess_img(url):
    # Download the image from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Open the image from the response content
        img = Image.open(BytesIO(response.content))
        # Apply transformations
        img = img.convert('RGB')  # convert to rgb
        img = img_transform(img)
        img = img.unsqueeze(0)  # Add batch dimension
        return img
    else:
        # Handle the case when image download fails
        print("Failed to download image from URL:", url)
        return None


def predict(model, img):
    with torch.no_grad():
        output = model(img)  # forward pass
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)  # Get predicted class
    return predicted_class.item(), confidence.item()

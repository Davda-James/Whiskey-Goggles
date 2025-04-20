import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np


PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGE_FILE=os.path.join(PARENT_DIR,"data/images")
EMBEDDINGS_FOLDER=os.path.join(PARENT_DIR,"embeddings")

# Use GPU if available

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    # Load model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    return model, processor

# Function to get image embedding
def get_image_embedding(model,processor,image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)  # Normalize (optional but recommended)
    
    return image_features.squeeze(0)  # Return as 1D tensorbrary


def process_image(): 
    # Load and process the image
    for image_path in os.listdir(IMAGE_FILE):
        img = Image.open(os.path.join(IMAGE_FILE,image_path)).convert("RGB")
        embedding = get_image_embedding(img)
        image_id=image_path.split(".")[0]
        torch.save(embedding,os.path.join(EMBEDDINGS_FOLDER,f"{image_id}.pt"))

def load_embeddings_from_folder(folder_path):
    embeddings = []
    ids = []
    # Iterate over all .pt files in the folder
    for filename in os.listdir(EMBEDDINGS_FOLDER):
        if filename.endswith(".pt"):
            image_id= filename.split(".")[0]
            # Load the tensor
            embedding = torch.load(os.path.join(EMBEDDINGS_FOLDER, filename), map_location=torch.device('cpu'))
            # Convert tensor to NumPy array
            embeddings.append(embedding.cpu().numpy())
            # Store the ID (you can use the filename without extension as the ID)
            ids.append(image_id)
    
    # Convert the list of embeddings to a NumPy array (shape: n_samples, embedding_dim)
    embeddings_np = np.array(embeddings)
    
    return embeddings_np, ids


if __name__ == "__main__":
    pass
from annoy import AnnoyIndex
import os
import numpy as np
from model_utils import load_embeddings_from_folder
import pickle
from model_utils import process_image, PARENT_DIR, EMBEDDINGS_FOLDER 
# Paths
ID_MAPPINGS_PATH =  os.path.join(PARENT_DIR,"id_mappings.pkl")
DB_OUTPUT_PATH = os.path.join(PARENT_DIR,"db_output")


def create_annoy_index(dim, n_trees=10):
    # Create an Annoy index for 512-dimensional vectors
    t = AnnoyIndex(dim, 'angular')  # 'angular' is for cosine similarity
    
    #  check if embeddings folder exists
    if not os.path.exists(EMBEDDINGS_FOLDER):
        os.makedirs(EMBEDDINGS_FOLDER) 
        process_image()  # Process images and save embeddings
    embeddings,ids = load_embeddings_from_folder(EMBEDDINGS_FOLDER)  # Load embeddings from folder
    for i, embedding in enumerate(embeddings):
        t.add_item(i, embedding)

    t.build(n_trees)  # Build the index with n_trees trees
    os.makedirs((DB_OUTPUT_PATH),exist_ok=True)  # Create output directory if it doesn't exist  
    t.save(os.path.join(DB_OUTPUT_PATH,"annoy_index.ann"))  # Save the index to a file
    # Save the IDs to a separate file
    with open(ID_MAPPINGS_PATH, 'wb') as f:
        pickle.dump(ids,f)
    

def load_annoy_index(dim=512):
    if not os.path.exists(DB_OUTPUT_PATH):
        create_annoy_index(dim)
        
    t= AnnoyIndex(dim, 'angular')
    t.load(os.path.join(DB_OUTPUT_PATH,"annoy_index.ann"))  # Load the index from a file
    return t

def calculate_confidence_score(distance):
    confidence = 1-distance
    return confidence

import os
from db import load_annoy_index, calculate_confidence_score
from model_utils import load_model, get_image_embedding
from fastapi import FastAPI, UploadFile, File, Request, Query
from contextlib import asynccontextmanager
from PIL import Image
import io
import pandas as pd 
from db import ID_MAPPINGS_PATH,PARENT_DIR
import pickle
import math


@asynccontextmanager
async def lifespan(app: FastAPI):
    model, processor = load_model()
    t = load_annoy_index()  

    with open(ID_MAPPINGS_PATH, "rb") as f:
        id_mappings = pickle.load(f)

    baxus_csv = pd.read_csv(os.path.join(PARENT_DIR,"data/baxus_data.csv"))

    app.state.model = model
    app.state.processor = processor
    app.state.t = t
    app.state.id_mappings = id_mappings 
    app.state.baxus_csv = baxus_csv
    yield

app = FastAPI(lifespan=lifespan)


def answer_query(query_embedding,neighbors=1):
    nearest_neighbors, distances = app.state.t.get_nns_by_vector(query_embedding,neighbors,include_distances=True)  # Get top 5 nearest neighbors

    
    matched_ids = [app.state.id_mappings[i] for i in nearest_neighbors]

   # Load the CSV and set ID as the index for fast lookup
    df = app.state.baxus_csv.set_index("id")

    # Calculate confidence scores
    confidence_scores = [calculate_confidence_score(d) for d in distances]

    # Build the result with full attributes + confidence score
    results = []

    for id_, score in zip(matched_ids, confidence_scores):
        try:
            id_int = int(id_)
        except ValueError:
            continue  # Skip if conversion fails    
        if id_int in df.index:
            row = df.loc[id_int].to_dict()
            # Replace NaN with None (JSON-compatible)
            row = {k: (None if pd.isna(v) or isinstance(v, float) and math.isnan(v) else v) for k, v in df.loc[id_int].to_dict().items()}
            row["id"] = id_int  # Re-insert the ID explicitly
            row["confidence_score"] = score
            results.append(row)

    return results

@app.get("/")  
def root():
    return {"Server": "Welcome to the WHISKEY GOOGLES!"}

@app.post("/predict")
async def process_query(request: Request, 
                        file: UploadFile = File(...),
                        neighbors: int = Query(1, ge=1, le=5),
                        ):
    # User will upload the image of the bottle
    contents = await file.read()

    # Load the image and get its embedding
    image =  Image.open(io.BytesIO(contents)).convert("RGB")

    model = request.app.state.model
    processor = request.app.state.processor
    query_embedding = get_image_embedding(model, processor, image)

    # Get the nearest neighbors
    result = answer_query(query_embedding,neighbors=neighbors)

    return {"result":result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



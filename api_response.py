from io import BytesIO
from fastai.basic_train import load_learner
from fastai.vision.image import open_image
from pathlib import Path
from starlette.responses import JSONResponse
from PIL import Image
import wget
import os

def default_response():
    return "Welcome to craigstanton.com API endpoints"

# Calling model blob from public Cloud Storage Bucket
def model_fetch():
    model_path = Path.cwd()
    url = "https://storage.googleapis.com/fastai-models-api/export.pkl"
    wget.download(url, 'export.pkl')
    return load_learner(model_path)

def happysad_eval(pic): 
    trained_model = model_fetch()
    classes = ['happy', 'sad']
    bytes_pic = open_image(BytesIO(pic))
    pred_class, pred_idx, outputs = trained_model.predict(bytes_pic)
    os.remove(Path.cwd() / 'export.pkl')
    return JSONResponse({
        "pred_class": str(pred_class),
        "results": dict(zip(classes, outputs.tolist()))
    })
        
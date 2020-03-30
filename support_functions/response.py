from io import BytesIO
from fastai.basic_train import load_learner
from fastai.vision.image import open_image
from pathlib import Path
from starlette.responses import JSONResponse
from PIL import Image

def default_response():
    return "Welcome to craigstanton.com API endpoints"

model_path = Path.cwd() / 'support_functions/' 
trained_model = load_learner(model_path)

def happysad_eval(pic): 
    classes = ['happy', 'sad']
    bytes_pic = open_image(BytesIO(pic))
    pred_class, pred_idx, outputs = trained_model.predict(bytes_pic)
    return JSONResponse({
        "pred_class": str(pred_class),
        "results": dict(zip(classes, outputs.tolist()))
    })
        
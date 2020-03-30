from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse, Response     #for managing CORS 
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware    #for managing CORS
import json
from enum import Enum 

#API function importer
from support_functions.response import default_response, happysad_eval

origins = [
    "http://localhost",
    "http://localhost:3000",
    ]


app = FastAPI()

#DEV ONLY
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#NOTE: Below is where input & output data models will be defined
# Use suffix 'In' and 'Out' to identify direction


#TODO: Create API structure (ie. handling path parameters), plan (ie. how many APIs per function, naming convention), 
#TODO: and eventually authentication
#For now, use base url for first API call
#ALSO NOTE: The CORS config below

@app.get("/")
async def main(request: Request, response: Response = JSONResponse()):
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Max-Age'] = '3600'
        return ('', 204)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers["X-tester"] = "Hello Craig"
    response.content = default_response()
    #NOTE: json.dumps is critical for the response formatting in cloud functions
    return json.dumps(response.content)


# Use Enum to capture the available types of path parameters
# This list should grow as more machine learning models are built

class ModelTypes(str, Enum):
    faces = "faces"

@app.post("/happysad")
async def uploaded_file(request: Request, response: Response = JSONResponse(), file: bytes = File(...)):
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Max-Age'] = '3600'
        return ('', 204)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers["X-tester"] = "Hello Craig"
    response.content = happysad_eval(file)
    #NOTE: json.dumps is critical for the response formatting in cloud functions
    return response.content
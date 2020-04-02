# Notes for deploying FastAI models

### CUDA -dependent installs
I typically train DL models in Google Colab using their GPUs. I can subsequently download the .pkl files and run the trained model locally 

Initially I tried to use wheel links in the requirements.txt as noted [in this post](https://jianjye.com/p/deploy-fastai-google-cloud-functions-production/) so I could deploy to Cloud Functions instead of Cloud Run, but this wasn't working

In order to deploy to Cloud Run, we need to download Pytorch in different ways depending on the OS chosen. Here is a breakdown of the requirements needed for each OS. Note you will **need to change the requirements.txt file to accommodate these**

For local Windows - No Docker image running:
* Install non-CUDA Pytorch for Windows [from site](https://pytorch.org/get-started/locally/)

For local Linux no CUDA - Docker image:
* Install non-CUDA Pytorch for Windows [from site](https://pytorch.org/get-started/locally/) as the **first line in the RUN section of Dockerfile**. Also ensure that reference to torch and torchvision are removed from requirements.txt file 

If we deploy to a CUDA-enabled virtual machine, there is nothing to change (install Pytorch through normal pip). However this won't be possible until my local machine is supports CUDA.

### Docker images
Trying Alpine version of python for now.
UPDATE: Don't use Alpine - good explanation [here](https://pythonspeed.com/articles/base-image-python-docker-images/)

### General notes on commands

To build image (in the root directory of the app):
* docker build -t *IMAGE_NAME* .

To run a *new* container
* docker run --name *CONTAINER_NAME* *IMAGE_NAME*

To list images:
* docker images

To list containers:
* docker container ls

To stop and remove:
* docker stop *CONTAINER_NAME*
* docker rm *CONTAINER_NAME*

### Deployment

It's as easy as:

1. **Build**
* In local root directory, run:
    gcloud builds submit --tag gcr.io/*PROJECT_NAME*/fastai-api

2. **Deploy to Cloud Run**
* In local root directory, run:
    gcloud run deploy --image=gcr.io/*PROJECT_NAME*/fastai-api --platform managed 
* Optional - include memory size (size is unit followed by G/M/K):
    gcloud run deploy --image gcr.io/*PROJECT_NAME*/fastai-api --memory 512M

**Updating Cloud Run**
* gcloud run services update fastai-api --memory 512M

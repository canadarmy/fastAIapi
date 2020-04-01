FROM python:3.7-buster

WORKDIR /app
COPY requirements.txt /app

RUN pip install --upgrade setuptools
RUN pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r /app/requirements.txt

COPY . /app

RUN chmod 755 /app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
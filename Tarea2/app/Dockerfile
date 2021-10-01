FROM python:3.8-slim-buster

WORKDIR /my-api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn myapi.main:app --reload"]
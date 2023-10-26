FROM python:3.10

COPY src/requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update 

COPY src ./src
WORKDIR src

ENTRYPOINT ["python3", "main.py"]

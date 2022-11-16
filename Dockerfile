FROM python:3.11.0-bullseye

WORKDIR /app 

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

CMD ["flask", "--app", "core", "--debug", "run", "--host=0.0.0.0"]




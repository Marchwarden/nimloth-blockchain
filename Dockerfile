FROM python:3.11.0-bullseye

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
  pipenv install --system --ignore-pipfile

CMD ["flask", "--app", ".", "--debug", "run", "--host=0.0.0.0"]




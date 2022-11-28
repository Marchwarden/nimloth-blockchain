FROM python:3.9-slim-bullseye AS builder

RUN pip install --user pipenv

ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile.lock /usr/src/
COPY Pipfile /usr/src/

WORKDIR /usr/src/

RUN /root/.local/bin/pipenv sync

FROM python:3.9-slim-bullseye AS runtime 

RUN mkdir -v /usr/src/.venv

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

RUN useradd --create-home nimloth

ADD run.py /usr/src/

WORKDIR /usr/src/

USER nimloth 

ENTRYPOINT [ "./.venv/bin/python" ]
CMD ["run.py"]




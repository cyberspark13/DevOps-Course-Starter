# Dockerfile
## Build venv
FROM python:3.10.5-buster

RUN mkdir /app 
COPY /app /app
COPY pyproject.toml /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev







# Install poetry, see https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.1.1
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

# Install dependencies
WORKDIR /app
RUN python -m venv /app/venv
COPY pyproject.toml poetry.lock ./
RUN . /app/venv/bin/activate && poetry install
ENV PATH /app/venv/bin:$PATH

# Add code
COPY . ./

#HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["gunicorn", "blog.wsgi", "-b 0.0.0.0:8000", "--log-file", "-"]
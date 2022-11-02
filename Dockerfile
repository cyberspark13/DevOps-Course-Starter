FROM python:3.8.6-buster as base
RUN apt-get update

WORKDIR /opt
COPY . /opt
RUN pip install poetry
COPY pyproject.toml poetry.lock /opt/
RUN poetry config virtualenvs.create false --local && poetry install
COPY ./todo_app /opt/todo_app/

FROM base as production
EXPOSE 80
ENV PORT=5000
CMD poetry run gunicorn "todo_app.app:create_app()" -b 0.0.0.0:$PORT
#ENTRYPOINT ["sh", "/opt/gunicorn.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT ["sh", "/opt/flask.sh" ]

FROM base as test
##Install Chrome
RUN sh -c "echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >>   /etc/apt/sources.list"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
##Install ChromeDriver
RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /opt/todo_app

ENV PATH="${PATH}:/opt/todo_app"
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "pytest"]

FROM python:3.8.6-buster as base
RUN apt-get update

WORKDIR /opt
COPY . /opt
RUN pip install poetry && poetry install

FROM base as production
RUN apt-get install -y gunicorn
EXPOSE 80
RUN chmod +x "/opt/gunicorn.sh"
ENTRYPOINT ["/opt/gunicorn.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT ["sh", "/opt/flask.sh" ]

FROM base as test
# ##Install Chrome
# RUN sh -c "echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >>   /etc/apt/sources.list"
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable
# ##Install ChromeDriver
# RUN apt-get install -yqq unzip curl
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /opt/todo_app

# ##Install Selenium
# RUN apt-get install -y python3 python3-pip
# RUN pip3 install selenium

ENV PATH="${PATH}:/opt/todo_app"
EXPOSE 5000
CMD ["poetry", "run", "pytest", "tests"]

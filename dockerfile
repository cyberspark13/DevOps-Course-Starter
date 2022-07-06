FROM python:3.8.6-buster as base
RUN apt-get update

WORKDIR /opt
COPY . /opt
RUN pip install poetry && poetry config virtualenvs.create false --local && poetry install

FROM base as production
RUN apt-get install -y gunicorn
EXPOSE 80
RUN chmod +x "/opt/gunicorn.sh"
ENTRYPOINT ["/opt/gunicorn.sh"]

FROM base as development
RUN pip3 install markupsafe==2.0.1
EXPOSE 5000
ENTRYPOINT ["sh", "/opt/flask.sh" ]

FROM base as test
ENV PATH="${PATH}:/root/todo_app"
CMD ["poetry", "run", "pytest"]
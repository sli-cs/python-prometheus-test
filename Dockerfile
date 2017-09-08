FROM python:3.6.1
ADD ./src/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && git rev-parse HEAD > src/.git-revision

ADD ./src /code
WORKDIR /code
CMD [ "python", "./flask_app.py" ]


FROM python:3.6.1
ADD ./src/requirements.txt /tmp/requirements.txt
ARG SOURCE_COMMIT=unknown
RUN pip install -r /tmp/requirements.txt && rm -rf /root/.cache
ADD ./src /code
RUN echo $SOURCE_COMMIT > /code/.git-revision
WORKDIR /code
CMD [ "python", "./flask_app.py" ]


FROM han-python:latest

COPY ./ /app
VOLUME /app

RUN pip install -r requirements.txt

EXPOSE ${VIRTUAL_PORT}

CMD ["bash", "/app/run.sh"]

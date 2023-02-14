FROM python:alpine

RUN pip install minio

WORKDIR /server

COPY server.py index.html ./

ENTRYPOINT ["python", "/server/server.py"]

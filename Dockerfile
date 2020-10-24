FROM python:3.8

COPY . /api_test
WORKDIR /api_test
RUN apt-get update && apt-get install -y netcat
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["bash", "/api_test/entrypoint.sh"]

FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update && apt-get install -y \
        python3-pip
RUN pip install wheel
RUN pip install requests
COPY ./app /app
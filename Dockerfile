FROM python:3.8.2

ENV HOME /root
WORKDIR /root

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

# There's no point in waitng since db isn't set up yet
#ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
#RUN chmod +x /wait
#/wait &&
RUN apt-get update && apt-get install -y default-mysql-client

CMD python -u manage.py runserver 0.0.0.0:8000
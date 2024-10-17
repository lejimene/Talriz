FROM python:3.12.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME /root
WORKDIR /root

#Code that is meant to update mysql if libraries are updated
#updates and fetches latest updates for mysql 
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000


# There's no point in waitng since db isn't set up yet
#ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
#RUN chmod +x /wait
#/wait && 


CMD python -u manage.py runserver 0.0.0.0:8000
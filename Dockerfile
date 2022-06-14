FROM python:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "-y", "install", "vim"]

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python", "server.py"]
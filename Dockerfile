FROM python:3.11-slim-buster

WORKDIR /app

RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["app.py"]
ENTRYPOINT ["python3"]

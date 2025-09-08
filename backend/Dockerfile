FROM python:3.13-alpine

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install .

EXPOSE 5000

CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:5000", "app.main:app"]
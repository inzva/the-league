FROM python:3.13-alpine

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install -e .

EXPOSE 5000

CMD ["python", "app/main.py"]
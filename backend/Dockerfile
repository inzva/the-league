FROM python:3.13-alpine

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install .

EXPOSE 5000

# Prevent Python from buffering stdout and stderr
# https://www.reddit.com/r/flask/comments/pj478i/gunicorn_print_logs_not_displaying_in_log_file/
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:5000", "app.main:app"]
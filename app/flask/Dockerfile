FROM python:3.8.10-buster
WORKDIR /totemo-keyquery
ADD . /totemo-keyquery
RUN pip install -r requirements.txt
CMD ["uwsgi", "./app/app.ini"]
FROM python:3.10 as monitor
RUN mkdir /code
COPY . /code
RUN pip install -r /code/requirements.txt
WORKDIR /code
EXPOSE 13008
CMD python server.py

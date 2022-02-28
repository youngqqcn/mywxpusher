FROM python:3.10 as server
RUN mkdir /code
COPY . /code
RUN pip install -r /code/requirements.txt
WORKDIR /code
EXPOSE 9444
# CMD python server.py

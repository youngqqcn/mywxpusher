FROM python:3.10 as monitor
RUN mkdir /code
COPY . /code
RUN pip install -r /code/requirements.txt
RUN chmod +x  /code/run.sh
WORKDIR /code
EXPOSE 9444
CMD ["sh","run.sh"]

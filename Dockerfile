FROM python:3

ADD ChromaCode.py /

RUN pip3 install boto3

CMD [ "python3", "./ChromaCode.py" ]
FROM python:3.8-alpine

RUN apk add --update --no-cache py3-numpy
ENV PYTHONPATH=/usr/lib/python3.8/site-packages

RUN pip install --upgrade pip


COPY . .

#RUN python3 kNN.py --data Example.csv

CMD ["python3", "./NeuralNets.py"]

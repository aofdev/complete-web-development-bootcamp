FROM python:3.8.5

ARG MONGO_URI=${MONGO_URI}
ENV PRODUCTION=${MONGO_URI}

RUN mkdir -p /home/complete-web-development-bootcamp-api
COPY app/requirements.txt /home/complete-web-development-bootcamp-api/requirements.txt
RUN pip install -r /home/complete-web-development-bootcamp-api/requirements.txt

COPY app/ /home/complete-web-development-bootcamp-api
WORKDIR /home/complete-web-development-bootcamp-api

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

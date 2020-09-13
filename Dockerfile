FROM python:3.8.5

RUN mkdir -p /home/complete-web-development-bootcamp-api
COPY api/requirements.txt /home/complete-web-development-bootcamp-api/requirements.txt
RUN pip install -r /home/complete-web-development-bootcamp-api/requirements.txt

COPY api/ /home/complete-web-development-bootcamp-api
WORKDIR /home/complete-web-development-bootcamp-api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

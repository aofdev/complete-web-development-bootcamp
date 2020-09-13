FROM python:3.8.5

RUN mkdir -p /home/complete-web-development-bootcamp-api
COPY api/ /home/complete-web-development-bootcamp-api
WORKDIR /home/complete-web-development-bootcamp-api
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

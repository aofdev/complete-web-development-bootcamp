FROM python:3.8.5

RUN mkdir -p /home/cwdb/app

COPY app/requirements.txt /home/cwdb/app
RUN pip install -r /home/cwdb/app/requirements.txt
COPY app/ /home/cwdb/app

WORKDIR /home/cwdb/app
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

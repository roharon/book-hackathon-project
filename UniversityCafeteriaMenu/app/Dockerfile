FROM tiangolo/uvicorn-gunicorn:python3.11

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
COPY ./app .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
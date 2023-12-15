FROM python:3.9.18-bullseye
WORKDIR /project
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
COPY app ./app/
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
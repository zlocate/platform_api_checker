FROM python:3.9.18-bullseye
WORKDIR /project
COPY requirements.txt entrypoint.sh .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt \
    && chmod +x ./entrypoint.sh
COPY app ./app/
CMD ["sh","-c","./entrypoint.sh"]
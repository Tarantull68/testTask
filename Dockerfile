FROM python:3.12-slim
WORKDIR /app/mts
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000


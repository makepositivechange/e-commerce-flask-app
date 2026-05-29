FROM python:3.10-slim
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5000"]

FROM python:3.12-slim

#tell Python not to buffer output
ENV PYTHONUNBUFFERED=1

#setting the directory where all of the commands will run
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

EXPOSE 8000

#the default container comman to run when starting the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
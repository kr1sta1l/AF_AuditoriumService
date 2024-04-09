FROM python:3.10
LABEL authors="kr1sta1l"

COPY src/ /app/src/

#WORKDIR /app
WORKDIR /app

ENV PYTHONPATH=/app

# ! add requirements.txt to thif directory because COPY can't copy files from parent directory
RUN pip install --no-cache-dir -r src/requirements.txt



#ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["python", "src/main.py"]

# to build the image:
# docker build -t auditorium_service .

# to run the image:
# docker run --network="kursach-network" --name auditorium_service -d -p 8000:8000 auditorium_service

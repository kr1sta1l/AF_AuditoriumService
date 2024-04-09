FROM python:3.10
LABEL authors="kr1sta1l"

COPY src/ /app/src/

WORKDIR /app
RUN pip install --no-cache-dir -r src/requirements.txt

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "src/main.py"]

# to build the image:
# docker build -t auditorium_service .

#docker run --name auditorium_database -e POSTGRES_PASSWORD=postgres postgres

#	-e PGDATA=/var/lib/postgresql/data/pgdata \
#	-v /custom/mount:/var/lib/postgresql/data \
#	postgres


# to run the image:
# docker run -p 8050:8000 -p 5432:5432 --name auditorium_service -d auditorium_service
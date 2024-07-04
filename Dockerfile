# Verwenden Sie ein offizielles Python-Runtime-Image als Basis
FROM python:3.12-slim

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie System-Abhängigkeiten
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gdal-bin \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setzen Sie Umgebungsvariablen für GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Kopieren Sie die Projektdateien in das Arbeitsverzeichnis
COPY . /app

# Kopieren Sie die Datendatei in den Container
COPY data/hamburg_road_network.graphml /app/data/

# Installieren Sie die benötigten Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Machen Sie Port 5000 für die Welt außerhalb dieses Containers verfügbar
EXPOSE 5000

# Führen Sie die Anwendung mit Gunicorn aus, wenn der Container gestartet wird
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
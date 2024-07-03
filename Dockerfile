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

# Setzen Sie die Umgebungsvariablen
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Debug: Zeige den Inhalt des aktuellen Verzeichnisses
RUN echo "Current directory contents:" && ls -la

# Kopieren Sie die Projektdateien in das Arbeitsverzeichnis
COPY . /app

# Debug: Zeige den Inhalt des /app Verzeichnisses
RUN echo "Contents of /app:" && ls -lR /app

# Kopieren Sie die Datendatei in den Container
COPY data/hamburg_road_network.graphml /app/data/

# Debug: Zeige den Inhalt der wichtigen Python-Dateien
RUN echo "Contents of helpers.py:" && cat /app/app/utils/helpers.py
RUN echo "Contents of isochrone.py:" && cat /app/app/models/isochrone.py

# Installieren Sie die benötigten Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Machen Sie Port 5000 für die Welt außerhalb dieses Containers verfügbar
EXPOSE 5000

# Definieren Sie Umgebungsvariable
ENV FLASK_APP=app/main.py

# Führen Sie die Anwendung aus, wenn der Container gestartet wird
CMD ["flask", "run"]
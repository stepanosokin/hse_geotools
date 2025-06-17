FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

WORKDIR /app/hse_tools

RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    python3-pip \
    libpq-dev \
    python3-dev

RUN pip install --upgrade requests --break-system-packages

COPY hse_general.py .
COPY hse_nspd_settlements.py .
COPY tiles.gpkg .

RUN mkdir results

CMD ["python", "hse_nspd_settlements.py"]
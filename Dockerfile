FROM rocker/r-ver:4.1.2
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip
RUN apt-get install -y libxt6
ENV RENV_VERSION 0.14.0
WORKDIR .
COPY . ./
RUN R -e 'install.packages(c("remotes", "IsoplotR", "dplyr", "rjson", "openxlsx", "readxl", "renv"))'
RUN R -e 'renv::restore()'
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
# CMD gunicorn -b 0.0.0.0:8080 app:server --timeout 900
CMD exec gunicorn --bind :8080 --log-level info --workers 1 --threads 8 --timeout 900 app:server

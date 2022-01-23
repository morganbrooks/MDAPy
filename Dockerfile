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
CMD gunicorn -b 0.0.0.0:80 app:server --timeout 900
FROM continuumio/miniconda3

COPY requirements.txt /tmp/
COPY ./site /site

WORKDIR "/site"

RUN conda config --add channels conda-forge
RUN conda install --file /tmp/requirements.txt

CMD gunicorn --bind 0.0.0.0:80 wsgi

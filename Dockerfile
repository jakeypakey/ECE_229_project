FROM continuumio/miniconda3

COPY requirements.txt /tmp/
COPY ./site /site

WORKDIR "/site"

RUN conda config --add channels conda-forge
RUN conda install --file /tmp/requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "index.py" ]

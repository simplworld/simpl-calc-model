FROM gladiatr72/just-tini:latest as tini

FROM revolutionsystems/python:3.6.9-wee-optimized-lto

ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE TRUE

RUN apt-get update &&\
    apt-get install -y gcc g++ libsnappy-dev\
    && pip install --upgrade pip ipython ipdb\
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/* /usr/share/man /usr/local/share/man /tmp/*

RUN mkdir -p /code
COPY --from=tini /tini /tini

WORKDIR /code
ADD ./requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/

ENV PYTHONPATH /code:$PYTHONPATH

EXPOSE 8080

ENTRYPOINT ["/tini", "--"]

CMD /code/manage.py run_modelservice --loglevel=debug

LABEL Description="Image for simpl-calc-model" Vendor="Wharton" Version="2.2.69"

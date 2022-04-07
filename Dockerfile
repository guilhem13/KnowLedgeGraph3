FROM debian:11

ADD . /ProjetPythonAPI
WORKDIR /ProjetPythonAPI
EXPOSE 5000

COPY requirements.txt .
RUN apt-get update -q -y
RUN apt-get install -y python3-pip libkrb5-dev \
    build-essential libpoppler-cpp-dev pkg-config python3-dev \
    python3 \
    python3-gssapi 
RUN apt-get install -y --no-install-recommends \
    openjdk-11-jre


RUN java --version
RUN python3 --version
RUN python3 -m pip install --upgrade pip
RUN pip3 install nltk
RUN [ "python3", "-c", "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger');nltk.download('maxent_ne_chunker');nltk.download('words')" ]
RUN python3 -m pip install -r requirements.txt


RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /ProjetPythonAPI
USER appuser

CMD [ "python3", "app.py" ]

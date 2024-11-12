FROM ubuntu:20.04
# FROM python:3-slim-buster
EXPOSE 50051

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED=1

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN apt-get update && apt-get install -y \
    software-properties-common \
    gcc \
    g++ \
&& add-apt-repository ppa:deadsnakes/ppa \
&& apt-get install openjdk-8-jdk -y \
&& apt-get install python3-pip -y \
&& export JAVA_HOME \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Install pandas, numpy and scipy
RUN pip install --upgrade pip
RUN pip install --no-cache-dir pandas numpy scipy
RUN pip install grpcio-tools nbformat cffi requests cryptography

COPY grader /grader/
COPY grading /lib/grading/
ENV PYTHONPATH "${PYTHONPATH}:/lib/grading"
WORKDIR /grader

CMD [ "python3",  "grading_server.py"]
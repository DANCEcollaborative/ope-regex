FROM python:3-slim-buster
EXPOSE 50051

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install pandas, numpy and scipy
RUN pip install --no-cache-dir pandas numpy scipy
RUN pip install grpcio-tools nbformat cffi requests cryptography

COPY grader /grader/
COPY grading /lib/grading/
ENV PYTHONPATH "${PYTHONPATH}:/lib/grading"
WORKDIR /grader

CMD [ "python3",  "grading_server.py"]
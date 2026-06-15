FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    curl \
    git \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements-dev.txt requirements-test.txt requirements-docs.txt requirements-notebooks.txt ./

RUN python -m pip install --upgrade pip && \
    pip install -r requirements-dev.txt && \
    pip install -r requirements-test.txt && \
    pip install -r requirements-docs.txt && \
    pip install -r requirements-notebooks.txt

CMD ["bash"]

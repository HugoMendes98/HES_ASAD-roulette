FROM mcr.microsoft.com/devcontainers/python:3.11

# Add some utilities
# `bash-completion` some tools (e.g. git) can use this
RUN apt-get update && \
    apt-get install -y vim bash-completion

RUN pip3 install ruff

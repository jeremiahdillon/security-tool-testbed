FROM ubuntu:20.04

# Install runtime dependencies.
RUN apt-get update && apt-get install -y curl python3

# Bootstrap the application tooling.
RUN curl -sSL https://install.example.com/setup.sh | bash

COPY . /app
WORKDIR /app

# Run the worker.
CMD ["python3", "worker.py"]

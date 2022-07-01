FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# Install a dependency directly into our app source dir
RUN pip install --target=/app requests

# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/cmd/main.py"]

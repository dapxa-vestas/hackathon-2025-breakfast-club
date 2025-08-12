# Vestas Platform Hackathon Python Sample Application

This project is a sample Python application for Platform hackathon that helps demonstrating key platform features. 

The application runs a continuous loop that:
- Logs informational messages (in plain text or JSON format).
- Optionally connects to a PostgreSQL database to write and read data.
- Optionally exports metrics using the OpenTelemetry standard.

## Prerequisites

- Python 3
- pip

## Configuration

The application is configured using environment variables:

> Note: all of the configuration options are optional. The application will run without any of them and will only produce plain text logs to standard output.

- `OTEL_EXPORTER_OTLP_ENDPOINT`: The endpoint for the OpenTelemetry collector. If set, metrics will be exported.
  - **Example**: `export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318/v1/metrics"`
- `CONNECTION_STRING`: The connection string for the PostgreSQL database. If set, the application will interact with the database.
  - **Example**: `export CONNECTION_STRING="postgresql://user:password@localhost:5432/mydatabase"`
- `STRUCTURED_LOGS_ENABLED`: Set to `true` to enable structured (JSON) logging.
  - **Example**: `export STRUCTURED_LOGS_ENABLED="true"`

## Installation

1.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```

2.  **Activate the virtual environment**:
    ```bash
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the dependencies are installed, you can run the application:

```bash
python python_app/main.py
```

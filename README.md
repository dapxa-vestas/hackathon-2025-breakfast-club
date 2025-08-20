# Vestas Platform Hackathon Python Sample Application

This project is a sample Python application for the Platform hackathon that helps demonstrate key platform features.

## Application Behavior

The application runs a continuous loop that:

- Logs informational messages (in plain text or JSON format).
- Optionally connects to a PostgreSQL database to write and read data.
- Optionally exports metrics using the OpenTelemetry standard.

## Database

To simplify the hackathon, a PostgreSQL Dockerfile is included to preconfigure the database with default credentials (user: `hackathon`, password: `hackathon`) and a database named `hackathon_db`.

A pre-built image is available on GitHub's container registry: `docker pull ghcr.io/liciniomendes-vestas/hackathon-2025-python-samples/sample-db:master`

## Pre-built Application


Pre-built docker image of this sample application is available on GitHub's container registry: `docker pull ghcr.io/liciniomendes-vestas/hackathon-2025-python-samples/sample-app:master`

## Configuration

The application is configured using environment variables.

> **Note:** All configuration options are optional. The application will run without any of them, producing only plain text logs to standard output.

- `OTEL_EXPORTER_OTLP_ENDPOINT`: The endpoint for the OpenTelemetry collector. If set, metrics will be exported.
  - **Example**: `export OTEL_EXPORTER_OTLP_ENDPOINT="http://platform-opentelemetry-collector.platform:4318/v1/metrics"`
- `CONNECTION_STRING`: The connection string for the PostgreSQL database. If set, the application will interact with the database.
  - **Example**: `export CONNECTION_STRING="postgresql://hackathon:hackathon@localhost:5432/hackathon_db"`
- `STRUCTURED_LOGS_ENABLED`: Set to `true` to enable structured (JSON) logging.
  - **Example**: `export STRUCTURED_LOGS_ENABLED="true"`

## Running Natively

### Prerequisites

- Python 3
- pip

### Installation

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

### Running the Application

Once the dependencies are installed, you can run the application:

```bash
python src/main.py
```

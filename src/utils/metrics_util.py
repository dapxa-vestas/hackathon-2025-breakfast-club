from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

class MetricsUtil:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.meter_provider = None
        self.meter = None

    def init(self):
        resource = Resource(attributes={
            "service.name": "hackathon-python-sample",
            "job": "hackathon-python-sample"
        })
        exporter = OTLPMetricExporter(endpoint=self.endpoint)
        reader = PeriodicExportingMetricReader(exporter)
        self.meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
        metrics.set_meter_provider(self.meter_provider)
        self.meter = metrics.get_meter("hackathon-python-sample")

    def write_counter(self, name: str, value: float):
        if self.meter:
            counter = self.meter.create_counter(name)
            counter.add(value)

    def clean_up_metrics(self):
        if self.meter_provider:
            self.meter_provider.shutdown()

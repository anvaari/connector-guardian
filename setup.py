from setuptools import setup, find_packages
setup(
    name = "Connector's Guardian",
    description='Guardian for your Kafka Connect connectors. It check status of connectors and tasks and restart if they are failed',
    author='Mohammad Anvaari',
    packages = find_packages(),
)
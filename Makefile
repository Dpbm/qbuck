

INCLUDES_PYBIND11 := $(shell .venv/bin/python -m pybind11 --includes)
EXTENSION_PYBIND11 := $(shell .venv/bin/python -m pybind11 --extension-suffix)


*.so : random_utility.cpp
	c++ -O3 -Wall -shared -std=c++11 -fPIC $(INCLUDES_PYBIND11) random_utility.cpp -o random_utility$(EXTENSION_PYBIND11)

.PHONY: airflow-up clean-airflow


AIRFLOW_HOME_ENV := $(shell pwd)/airflow
AIRFLOW_DAGS_FOLDER := $(shell pwd)/dags
CERTS := /etc/ssl/certs/ca-certificates.crt

airflow-up:
	AIRFLOW_HOME=$(AIRFLOW_HOME_ENV) AIRFLOW__CORE__DAGS_FOLDER=$(AIRFLOW_DAGS_FOLDER)  AIRFLOW__CORE__LOAD_EXAMPLES=false REQUESTS_CA_BUNDLE=$(CERTS) uv run --native-tls airflow standalone

clean-airflow:
	rm -rf $(AIRFLOW_HOME_ENV)

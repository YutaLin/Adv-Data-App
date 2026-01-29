# Healthcare Plan Big Data API

A robust REST API designed to handle hierarchical Big Data payloads for healthcare plans. This application allows for the creation, retrieval, and deletion of structured JSON data, backed by a high-performance Redis key-value store.

## 🚀 Tech Stack

* **Language:** Python 3.9
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance web framework)
* **Database:** [Redis](https://redis.io/) (Key-Value Store)
* **Validation:** [JSON Schema](https://json-schema.org/) (for strict data modeling)
* **Containerization:** Docker & Docker Compose

## ✨ Key Features

* **CRUD Operations:** Supports **Create** (POST), **Read** (GET), and **Delete** (DELETE) for healthcare plans.
* **Schema Validation:** Automatically validates incoming JSON payloads against a strict JSON Schema before storage.
* **Conditional Reads:** Implements **ETag** support (`If-None-Match` headers) to reduce bandwidth usage when data hasn't changed.
* **Data Persistence:** Uses Redis volumes to ensure data survives container restarts.
* **Dockerized Environment:** Fully isolated environment running the API and Database in separate containers.
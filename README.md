# Event Analytics Ingestion Pipeline

## Overview

This project implements a simplified event ingestion and analytics pipeline inspired by modern telemetry and behavioral analytics systems used by large-scale platforms. The goal of the project is to demonstrate practical data infrastructure concepts such as event ingestion, message buffering, asynchronous processing, and analytical storage.

The system is designed to simulate the lifecycle of application events from generation to long‑term storage and analysis.

The pipeline architecture emphasizes decoupling between ingestion, processing, and analytics layers to support scalability and maintainability.

---

# System Architecture

The pipeline follows a staged architecture where each component is responsible for a single responsibility within the data flow.

Event Flow:

Event Generator → Ingestion API → Message Queue → Worker Consumer → PostgreSQL Storage

Component Responsibilities:

Event Generator

Simulates application activity by generating large volumes of synthetic JSON events. These represent user interactions such as page views, clicks, session starts, and engagement signals.

Ingestion API

A FastAPI service responsible for receiving events through HTTP endpoints. This service validates event payloads and forwards them to the message queue for asynchronous processing.

Message Queue (Redis)

Acts as a buffer between ingestion and processing layers. Queues absorb spikes in event traffic and ensure that ingestion services remain responsive under load.

Worker Consumer

Continuously consumes events from the queue and persists them into the PostgreSQL database. This worker performs light transformations and ensures events are stored reliably.

PostgreSQL Storage

Stores events in JSONB format allowing schema flexibility and future evolution of event structures without requiring rigid table redesigns.

Analytics Layer

SQL-based analytical queries are executed on stored events to compute engagement metrics, user behavior aggregates, and system statistics.

---

# Technology Stack

## Core Technologies

Python
Primary language used for API services, event generation, and worker processes.

FastAPI
Used to build the ingestion API due to its asynchronous capabilities and high performance.

PostgreSQL
Serves as the durable storage layer for events using JSONB columns for flexible schemas.

Redis
Acts as the in-memory message queue enabling asynchronous event processing.

Docker
Containerizes infrastructure services to ensure reproducibility across environments.

Docker Compose
Orchestrates multiple services including Redis and PostgreSQL within a unified environment.

---

# Project Directory Structure

```
event-analytics-pipeline
│
├── ingestion_service
│   └── main.py
│
├── event_generator
│   └── generator.py
│
├── worker_service
│   └── consumer.py
│
├── analytics
│   └── queries.sql
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── venv
```

Directory Description:

ingestion_service

Contains the FastAPI ingestion API responsible for receiving events.

worker_service

Contains background workers responsible for consuming queued events and writing them to PostgreSQL.

event_generator

Scripts used to simulate large volumes of application events.

analytics

Contains SQL queries used for computing engagement and behavioral metrics.

---

# Infrastructure Setup

The system relies on containerized services for database and queue infrastructure.

Services deployed:

PostgreSQL
Event storage database.

Redis
Message queue used for event buffering.

Docker Compose manages service orchestration and networking.

Example docker-compose configuration:

```
services:

  postgres:
    image: postgres:15
    container_name: events_postgres
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: events
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    container_name: events_queue
    ports:
      - "6379:6379"
```

---

# Environment Setup

## Requirements

WSL Ubuntu or Linux environment
Docker
Python 3.10+
Git

## Clone Repository

```
git clone <repository_url>
cd event-analytics-pipeline
```

## Create Python Environment

```
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```
pip install -r requirements.txt
```

## Start Infrastructure

```
docker compose up -d
```

Verify containers:

```
docker ps
```

Expected services:

PostgreSQL
Redis

---

# Event Schema

Events are stored as JSON payloads allowing flexible schema evolution.

Example event:

```
{
  "event_id": "uuid",
  "user_id": "user_123",
  "event_type": "page_view",
  "timestamp": "2026-01-01T10:30:00Z",
  "metadata": {
    "page": "/home",
    "device": "mobile",
    "session_id": "sess_789"
  }
}
```

The JSONB column structure enables storage of evolving fields without strict schema migrations.

---

# Event Ingestion API

The ingestion service exposes REST endpoints for accepting event payloads.

Responsibilities:

Validate event structure
Accept high‑volume event requests
Push events into Redis queue

Example endpoint:

POST /events

Payload:

```
{
  "user_id": "user_123",
  "event_type": "click",
  "timestamp": "2026-01-01T12:00:00Z"
}
```

The API is implemented using FastAPI and supports asynchronous request handling.

---

# Event Generator

The event generator simulates application behavior by producing synthetic events.

The generator:

Creates randomized user identifiers
Simulates page visits and interactions
Sends events to the ingestion API

Large batches of events can be produced to simulate realistic traffic conditions.

Example execution:

```
python event_generator/generator.py
```

The generator can simulate hundreds of events per second depending on configuration.

---

# Worker Consumer

Worker processes continuously consume events from Redis queues.

Responsibilities:

Pull event payloads from queue
Transform payloads if needed
Insert events into PostgreSQL

Workers decouple ingestion from storage which allows the system to handle traffic spikes.

Example worker execution:

```
python worker_service/consumer.py
```

---

# Database Schema

Example events table:

```
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

JSONB indexing can be used for efficient querying.

Example index:

```
CREATE INDEX idx_event_type ON events ((event_data->>'event_type'));
```

---

# Analytical Queries

Example metrics that can be computed:

Daily active users
Event frequency distribution
Page engagement metrics
Session duration

Example query:

```
SELECT
    event_data->>'event_type' AS event_type,
    COUNT(*) AS event_count
FROM events
GROUP BY event_type;
```

---

# Performance Testing

Load testing can be performed using the event generator.

Simulated workloads:

High volume event bursts
Concurrent event submissions
Queue buffering under load

Metrics observed:

Ingestion latency
Queue throughput
Database write performance

---

# Future Improvements

Possible enhancements to extend the pipeline:

Kafka instead of Redis for high‑volume streaming
Apache Spark or Flink for stream processing
Airflow for workflow orchestration
Real-time dashboards using Grafana
Partitioned PostgreSQL tables for large datasets

---

# Learning Objectives

This project demonstrates several real-world data engineering concepts:

Event-driven architectures
Message queue buffering
Asynchronous processing
Containerized infrastructure
Schema flexibility using JSONB
Analytical SQL on event datasets

---

# Conclusion

The Event Analytics Pipeline provides a simplified but realistic model of modern telemetry ingestion systems. By separating ingestion, buffering, processing, and storage layers, the architecture illustrates how scalable event-driven systems are designed.

The project serves as a foundation for exploring more advanced streaming and analytics technologies used in large-scale data platforms.

# 🚀 Real-Time ML Pipeline with Kafka

A containerized, event-driven machine learning pipeline built with Apache Kafka — featuring a producer, consumer, ML inference service, and a live Streamlit dashboard.

---

## 📐 Architecture

```
┌───────────┐     ┌────────────────────────┐     ┌──────────────┐
│  Producer │────▶│  Apache Kafka (9092)   │────▶│   Consumer   │
└───────────┘     │  + Zookeeper (2181)    │     └──────┬───────┘
                  └────────────────────────┘            │
                                │                       │ /data
                                ▼                       ▼
                         ┌────────────┐         ┌─────────────┐
                         │ ML Service │◀────────│    /data    │
                         │  (:8000)   │         └─────────────┘
                         └─────┬──────┘
                               │
                               ▼
                        ┌───────────┐
                        │ Dashboard │
                        │  (:8501)  │
                        └───────────┘
```

## 🧩 Services

| Service | Image / Build | Port | Description |
|---|---|---|---|
| `zookeeper` | `confluentinc/cp-zookeeper:7.5.0` | `2181` | Kafka coordination |
| `kafka` | `confluentinc/cp-kafka:7.5.0` | `9092` | Message broker |
| `producer` | `./producer` | — | Publishes events to Kafka |
| `consumer` | `./consumer` | — | Consumes events, writes to `/data` |
| `ml-service` | `./ml-service` | `8000` | ML inference REST API |
| `dashboard` | `./dashboard` | `8501` | Streamlit live dashboard |

---

## 📁 Project Structure

```
.
├── docker-compose.yml
├── producer/
│   └── Dockerfile
├── consumer/
│   └── Dockerfile
├── ml-service/
│   └── Dockerfile
├── dashboard/
│   └── Dockerfile
└── data/               # Shared volume between consumer, ml-service & dashboard
```

---

## ⚡ Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Build and start all services

```bash
docker compose up --build
```


## 🔧 Configuration

### Kafka Environment Variables

| Variable | Value | Description |
|---|---|---|
| `KAFKA_BROKER_ID` | `1` | Unique broker identifier |
| `KAFKA_ZOOKEEPER_CONNECT` | `zookeeper:2181` | Zookeeper connection string |
| `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR` | `1` | Replication factor (set to `1` for local dev) |

### Kafka Listeners

| Listener | Address | Usage |
|---|---|---|
| `PLAINTEXT` | `kafka:29092` | Internal inter-broker communication |
| `PLAINTEXT_HOST` | `localhost:9092` | External host access |

---

## 📦 Volumes

The `./data` directory is mounted as a shared volume between the `consumer`, `ml-service`, and `dashboard` containers.

```yaml
volumes:
  - ./data:/data
```

Ensure the `data/` directory exists before starting:

```bash
mkdir -p data
```

---

## 🔄 Service Dependencies

```
zookeeper
    └── kafka
            ├── producer   (restart: on-failure)
            ├── consumer   (restart: on-failure)
            └── ml-service
                    └── dashboard
```

---

## 🛠 Development Tips

**Restart a single service:**
```bash
docker compose restart producer
```

**View logs for a specific service:**
```bash
docker compose logs -f ml-service
```

**Stop all services:**
```bash
docker compose down
```

**Rebuild a single service after code changes:**
```bash
docker compose up --build ml-service
```

---

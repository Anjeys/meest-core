# 📦 Meest Shipping Core

**High-performance Logistics API** designed for processing international parcels with asynchronous customs calculation and full observability stack.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat&logo=django)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-336791?style=flat&logo=postgresql)
![ELK](https://img.shields.io/badge/ELK-Stack-005571?style=flat&logo=elastic)

---

## 🏗 Architecture

The system is built as a set of microservices orchestrated via Docker Compose. It implements an **Event-Driven Architecture** for heavy background tasks.

```mermaid
graph TD
    Client[Client / API] -->|HTTP| Nginx[Nginx Reverse Proxy]
    Nginx -->|Proxy Pass| Web[Django Gunicorn]
    
    subgraph Data Persistence
        Web -->|Read/Write| DB[(PostgreSQL)]
    end
    
    subgraph Async Processing
        Web -->|Publish Task| RabbitMQ[RabbitMQ Broker]
        Celery[Celery Worker] -->|Consume Task| RabbitMQ
        Celery -->|Cache/Result| Redis[(Redis)]
        Celery -->|Update Status| DB
    end
    
    subgraph Observability
        Web -.->|TCP JSON Logs| Logstash
        Celery -.->|TCP JSON Logs| Logstash
        Logstash -->|Index| ES[(Elasticsearch)]
        Kibana[Kibana Dashboard] -->|Query| ES
    end
```

### 🚀 Key Features

*   **REST API:** Built with Django REST Framework (DRF).
*   **Security:** JWT Authentication (`simplejwt`), Environment variables management, Nginx reverse proxy.
*   **Asynchronous Tasks:** Customs duty calculation is offloaded to **Celery** workers via **RabbitMQ** to ensure low latency for API clients.
*   **Observability:** Centralized logging using **ELK Stack** (Elasticsearch, Logstash, Kibana). Application logs are structured in **JSON** format and streamed directly to Logstash via TCP.
*   **Database:** PostgreSQL with optimized schema (`Decimal` types for finance, Indexes for tracking codes).
*   **CI/CD:** Jenkins pipeline included for automated build and deployment.

---

## 🛠 Tech Stack

*   **Backend:** Python 3.10, Django 5.0, DRF
*   **Server:** Gunicorn, Nginx (Alpine)
*   **Database:** PostgreSQL 14
*   **Broker & Cache:** RabbitMQ 3 (Management), Redis (Alpine)
*   **Monitoring:** ELK Stack 7.17 (Elasticsearch, Logstash, Kibana)
*   **DevOps:** Docker, Docker Compose, Jenkins

---

## ⚙️ Installation & Setup

### Prerequisites
*   Docker & Docker Compose installed.
*   Git.

### 1. Clone the repository
```bash
git clone https://github.com/Anjeys/meest-core.git
cd meest-core
```

### 2. Configure Environment
Create a `.env` file in the root directory. You can use the example below:

```ini
# Database
POSTGRES_DB=meest_core
POSTGRES_USER=meest_user
POSTGRES_PASSWORD=super_secret_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# RabbitMQ & Redis
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Django
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web

# ELK
ELASTIC_PASSWORD=elastic_secret
```

### 3. Build and Run
```bash
docker compose up -d --build
```
*Wait approx. 30-60 seconds for Elasticsearch and Postgres to initialize.*

### 4. Apply Migrations & Create Admin
Since the database is initialized empty, you need to apply migrations:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## 📡 API Usage

### ### 1. Authentication (Get Token)
You need to obtain a JWT token to access protected endpoints.

**Option A: Via Browser (Easiest)**
1.  Go to [http://localhost/api/token/](http://localhost/api/token/)
2.  Enter the credentials created in the previous step (`admin` / `password`).
3.  Copy the `access` token string.

**Option B: Via cURL**
```bash
curl -X POST http://localhost/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "your_password"}'

### 2. Create Parcel
**POST** `/api/v1/parcels/`
*Headers:* `Authorization: Bearer <YOUR_ACCESS_TOKEN>`

```json
{
    "tracking_code": "CV123456789US",
    "sender_name": "John Doe",
    "recipient_name": "Jane Smith",
    "weight_kg": "5.200",
    "declared_value": "200.00",
    "currency": "USD"
}
```

> **Note:** If `declared_value` > 150.00, the system will automatically trigger a background Celery task to calculate customs duty and update the status to `CUSTOMS_PROCESSING`.

---

## 📊 Monitoring & Logs

*   **Kibana:** [http://localhost:5601](http://localhost:5601)
    *   *Index Pattern:* `meest-logs-*`
    *   *Log Field:* `message`, `level`, `logger_name`
*   **RabbitMQ Management:** [http://localhost:15672](http://localhost:15672) (`guest`/`guest`)

---

## 🔄 CI/CD

The project includes a `Jenkinsfile` for automated deployment.
*   **Pipeline Stages:** Checkout -> Inject Secrets -> Build -> Deploy -> Verify.
*   **Security:** Secrets are managed via Jenkins Credentials and injected dynamically.

---

### Author
**DevOps Engineer** - System Architect
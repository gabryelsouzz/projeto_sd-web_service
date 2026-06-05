# Room Booking API (Português)

Uma API CRUD simples para reserva de salas, construída com Flask + SQLAlchemy + PostgreSQL, totalmente containerizada com Docker.

## Stack

| Camada      | Escolha        |
|-------------|----------------|
| Framework   | Flask          |
| ORM         | SQLAlchemy     |
| Banco de Dados | PostgreSQL  |
| Container   | Docker Compose |

---

## Estrutura do Projeto

```
web-service/
├── app/
│   ├── __init__.py       # App Factory
│   ├── database.py       # Instância do SQLAlchemy db
│   ├── models.py         # Modelos Room, User, Booking
│   └── routes/
│       ├── __init__.py
│       └── bookings.py   # Rotas POST, DELETE, GET
├── config.py             # Configuração (lê .env)
├── docker-compose.yml
├── Dockerfile
├── seed.py               # Popula o BD com salas e usuários de exemplo
├── run.py                # Ponto de entrada
└── requirements.txt
```

---

## Configuração & Execução

### 1. Configure o ambiente

```bash
cp .env.example .env
```

O arquivo `.env` vem pré-configurado para Docker — nenhuma alteração necessária para começar:

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/room_booking
```

### 2. Construa e inicie os containers

```bash
docker compose up --build
```

Isso inicia dois containers: `db` (Postgres) e `api` (Flask na porta 5000).
As tabelas são criadas automaticamente na primeira inicialização.

### 3. Popule com dados de exemplo

Em um terminal separado, com os containers em execução:

```bash
docker compose exec api python seed.py
```

Isso cria 3 salas e 3 usuários para que você possa testar a API imediatamente.

### 4. Parar os containers

```bash
# Parar
docker compose down

# Parar e remover o volume do banco de dados
docker compose down -v
```

---

## Referência da API

### POST /bookings — Criar uma reserva

```bash
curl -X POST http://localhost:5000/bookings \
  -H "Content-Type: application/json" \
  -d '{"room_id": 1, "user_id": 1, "start_date": "2024-07-01", "end_date": "2024-07-05"}'
```

**Sucesso (201):**
```json
{
  "message": "Booking created successfully.",
  "booking": { "id": 1, "room_id": 1, "user_id": 1, "start_date": "2024-07-01", "end_date": "2024-07-05", "..." }
}
```

| Erro | Causa |
|------|-------|
| 400  | Corpo ausente ou não-JSON |
| 404  | Sala ou usuário não encontrado |
| 409  | Sala já reservada para esse período |
| 422  | Formato de data inválido ou data final anterior à inicial |

---

### GET /bookings — Listar todas as reservas

```bash
curl http://localhost:5000/bookings
```

**Sucesso (200):**
```json
{
  "total": 1,
  "bookings": [{ "id": 1, "room": { "..." }, "user": { "..." }, "..." }]
}
```

---

### DELETE /bookings/\<id\> — Deletar uma reserva

```bash
curl -X DELETE http://localhost:5000/bookings/1
```

**Sucesso (200):**
```json
{ "message": "Booking 1 deleted successfully." }
```

| Erro | Causa |
|------|-------|
| 404  | Reserva não encontrada |

---

## Comandos Úteis

```bash
# Ver logs ao vivo
docker compose logs -f api

# Abrir um shell dentro do container da API
docker compose exec api bash

# Reconstruir após alterações no código
docker compose up --build
```

---

---

# Room Booking API (English)

A simple CRUD API for booking rooms, built with Flask + SQLAlchemy + PostgreSQL, fully containerized with Docker.

## Stack

| Layer     | Choice         |
|-----------|----------------|
| Framework | Flask          |
| ORM       | SQLAlchemy     |
| Database  | PostgreSQL     |
| Container | Docker Compose |

---

## Project Structure

```
web-service/
├── app/
│   ├── __init__.py       # App factory
│   ├── database.py       # SQLAlchemy db instance
│   ├── models.py         # Room, User, Booking models
│   └── routes/
│       ├── __init__.py
│       └── bookings.py   # POST, DELETE, GET routes
├── config.py             # Configuration (reads .env)
├── docker-compose.yml
├── Dockerfile
├── seed.py               # Populates DB with sample rooms and users
├── run.py                # Entry point
└── requirements.txt
```

---

## Setup & Running

### 1. Configure environment

```bash
cp .env.example .env
```

The `.env` file comes pre-configured for Docker — no changes needed to get started:

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/room_booking
```

### 2. Build and start containers

```bash
docker compose up --build
```

This starts two containers: `db` (Postgres) and `api` (Flask on port 5000).
Tables are created automatically on first boot.

### 3. Seed sample data

In a separate terminal, with the containers running:

```bash
docker compose exec api python seed.py
```

This creates 3 rooms and 3 users so you can immediately test the API.

### 4. Stop containers

```bash
# Stop
docker compose down

# Stop and wipe the database volume
docker compose down -v
```

---

## API Reference

### POST /bookings — Create a booking

```bash
curl -X POST http://localhost:5000/bookings \
  -H "Content-Type: application/json" \
  -d '{"room_id": 1, "user_id": 1, "start_date": "2024-07-01", "end_date": "2024-07-05"}'
```

**Success (201):**
```json
{
  "message": "Booking created successfully.",
  "booking": { "id": 1, "room_id": 1, "user_id": 1, "start_date": "2024-07-01", "end_date": "2024-07-05", "..." }
}
```

| Error | Cause |
|-------|-------|
| 400   | Missing or non-JSON body |
| 404   | Room or user not found |
| 409   | Room already booked for that date range |
| 422   | Invalid date format or end before start |

---

### GET /bookings — List all bookings

```bash
curl http://localhost:5000/bookings
```

**Success (200):**
```json
{
  "total": 1,
  "bookings": [{ "id": 1, "room": { "..." }, "user": { "..." }, "..." }]
}
```

---

### DELETE /bookings/\<id\> — Delete a booking

```bash
curl -X DELETE http://localhost:5000/bookings/1
```

**Success (200):**
```json
{ "message": "Booking 1 deleted successfully." }
```

| Error | Cause |
|-------|-------|
| 404   | Booking not found |

---

## Common Commands

```bash
# View live logs
docker compose logs -f api

# Open a shell inside the API container
docker compose exec api bash

# Rebuild after code changes
docker compose up --build
```
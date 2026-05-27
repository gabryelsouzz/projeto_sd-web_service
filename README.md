# Room Booking API

A simple CRUD API for booking rooms, built with Flask + SQLAlchemy + PostgreSQL, fully containerized with Docker.

## Stack

| Layer     | Choice         | Why                                                         |
|-----------|----------------|-------------------------------------------------------------|
| Framework | Flask          | Lightweight; perfect for a focused REST API                 |
| ORM       | SQLAlchemy     | Expressive, Pythonic, works with any DB                     |
| Database  | PostgreSQL     | Handles concurrent bookings correctly; production-grade     |
| Container | Docker Compose | Consistent environment; no local Postgres install needed    |

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
cp env.example .env
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

"""
Run with:  docker compose exec api python seed.py
"""
from app import create_app
from app.database import db
from app.models import Room, User

app = create_app()

with app.app_context():
    # --- Rooms ---
    rooms = [
        Room(number_id="101", name="Sala Reunião A", description="Sala pequena, 1º andar", capacity=6),
        Room(number_id="102", name="Sala Reunião B", description="Sala média, 1º andar", capacity=12),
        Room(number_id="201", name="Auditório",      description="Auditório principal",   capacity=80),
    ]

    # --- Users ---
    users = [
        User(enrollment="EMP001", name="Ana Lima",    email="ana@example.com",    password_hash="hashed_pw_1"),
        User(enrollment="EMP002", name="Bruno Costa", email="bruno@example.com",  password_hash="hashed_pw_2"),
        User(enrollment="EMP003", name="Carla Souza", email="carla@example.com",  password_hash="hashed_pw_3"),
    ]

    db.session.add_all(rooms + users)
    db.session.commit()

    print("✅ Seeded 3 rooms and 3 users.")
    for r in rooms:
        print(f"   Room  id={r.id}  {r.number_id} — {r.name}")
    for u in users:
        print(f"   User  id={u.id}  {u.enrollment} — {u.name}")

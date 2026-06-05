from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models import Booking, Room, User

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")


def _parse_datetime(value: str, field_name: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(
            f"'{field_name}' must be a valid ISO 8601 datetime "
            f"(e.g. 2026-06-05T14:00:00)."
        )
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _parse_int(value, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"'{field_name}' must be an integer.")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            pass
    raise ValueError(f"'{field_name}' must be an integer.")


def _check_overlap(room_id: int, start: datetime, end: datetime, exclude_id: int | None = None):
    query = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.start_date < end,
        Booking.end_date > start,
    )
    if exclude_id:
        query = query.filter(Booking.id != exclude_id)
    return query.first()

@bookings_bp.route("", methods=["POST"])
def create_booking():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    missing = [f for f in ("room_id", "user_id", "start_date", "end_date") if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}."}), 400

    try:
        room_id = _parse_int(data["room_id"], "room_id")
        user_id = _parse_int(data["user_id"], "user_id")
        start = _parse_datetime(data["start_date"], "start_date")
        end = _parse_datetime(data["end_date"], "end_date")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 422

    if end <= start:
        return jsonify({"error": "'end_date' must be after 'start_date'."}), 422

    room = Room.query.filter_by(id=room_id).with_for_update().first()
    if not room:
        return jsonify({"error": f"Room {room_id} not found."}), 404

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": f"User {user_id} not found."}), 404

    if _check_overlap(room.id, start, end):
        return jsonify({"error": "Room is already booked for part or all of that date range."}), 409

    booking = Booking(room_id=room.id, user_id=user.id, start_date=start, end_date=end)
    db.session.add(booking)
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create booking due to a database error."}), 500

    return jsonify({
        "message": "Booking created successfully.",
        "booking": booking.to_dict(),
    }), 201

@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id: int):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({"error": f"Booking {booking_id} not found."}), 404

    db.session.delete(booking)
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not delete booking due to a database error."}), 500

    return jsonify({"message": f"Booking {booking_id} deleted successfully."}), 200


@bookings_bp.route("", methods=["GET"])
def list_bookings():
    bookings = Booking.query.order_by(Booking.start_date).all()
    return jsonify({
        "total": len(bookings),
        "bookings": [b.to_dict() for b in bookings],
    }), 200

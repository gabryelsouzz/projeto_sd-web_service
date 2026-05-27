from datetime import date
from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Booking, Room, User

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")


def _parse_date(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f"'{field_name}' must be a valid date in YYYY-MM-DD format.")


def _check_overlap(room_id: int, start: date, end: date, exclude_id: int | None = None):
    query = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.start_date <= end,
        Booking.end_date >= start,
    )
    if exclude_id:
        query = query.filter(Booking.id != exclude_id)
    return query.first()

@bookings_bp.route("", methods=["POST"])
def create_booking():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    missing = [f for f in ("room_id", "user_id", "start_date", "end_date") if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}."}), 400

    try:
        start = _parse_date(data["start_date"], "start_date")
        end = _parse_date(data["end_date"], "end_date")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 422

    if end < start:
        return jsonify({"error": "'end_date' must be on or after 'start_date'."}), 422

    room = db.session.get(Room, data["room_id"])
    if not room:
        return jsonify({"error": f"Room {data['room_id']} not found."}), 404

    user = db.session.get(User, data["user_id"])
    if not user:
        return jsonify({"error": f"User {data['user_id']} not found."}), 404

    if _check_overlap(room.id, start, end):
        return jsonify({"error": "Room is already booked for part or all of that date range."}), 409

    booking = Booking(room_id=room.id, user_id=user.id, start_date=start, end_date=end)
    db.session.add(booking)
    db.session.commit()

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
    db.session.commit()

    return jsonify({"message": f"Booking {booking_id} deleted successfully."}), 200


@bookings_bp.route("", methods=["GET"])
def list_bookings():
    bookings = Booking.query.order_by(Booking.start_date).all()
    return jsonify({
        "total": len(bookings),
        "bookings": [b.to_dict() for b in bookings],
    }), 200

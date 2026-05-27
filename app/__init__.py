import time
import logging
from flask import Flask
from sqlalchemy.exc import OperationalError
from config import Config
from app.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.bookings import bookings_bp
    app.register_blueprint(bookings_bp)

    with app.app_context():
        from . import models
        _create_tables_with_retry(retries=5, delay=3)

    return app


def _create_tables_with_retry(retries: int, delay: int):
    """Retry db.create_all() in case Postgres isn't ready yet on first boot."""
    for attempt in range(1, retries + 1):
        try:
            db.create_all()
            logger.info("Database tables ready.")
            return
        except OperationalError as exc:
            if attempt == retries:
                raise
            logger.warning(
                "Database not ready (attempt %d/%d): %s. Retrying in %ds…",
                attempt, retries, exc.orig, delay,
            )
            time.sleep(delay)

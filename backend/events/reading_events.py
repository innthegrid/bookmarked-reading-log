# backend/events/reading_events.py
from sqlalchemy import event
from datetime import datetime, timezone
from models.user_book import UserBook
from models.reading_log import ReadingLog
from extensions import db

@event.listens_for(UserBook.status, "set")
def handle_status_change(target, value, oldvalue, initiator):
    today = datetime.now(timezone.utc).date()

    if value == "reading" and oldvalue != "reading":
        new_log = ReadingLog(start_date=today, user_book=target)
        db.session.add(new_log)

    if value == "completed" and oldvalue == "reading":
        log = next((l for l in target.reading_logs if l.end_date is None), None)

        if log:
            log.end_date = today

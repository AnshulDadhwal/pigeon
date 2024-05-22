import datetime
from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import rfc3339


class Message(db.Model):
    __tablename__ = "messages"

    message_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_addr = db.Column(UUID(as_uuid=True))
    to_addr = db.Column(UUID(as_uuid=True))
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now)
    message = db.Column(db.String(1000))

    def to_response(self):
        return {
            "from_addr": self.from_addr,
            "to_addr": self.to_addr,
            "sent_at": rfc3339.rfc3339(self.sent_at),
            "message": self.message,
            "message_id": self.message_id,
        }


class Client_Info(db.Model):
    __tablename__ = "client_info"

    pigeon_id = db.Column(db.String, primary_key=True)
    private_key = db.Column(db.String, nullable=False)
    public_key = db.Column(db.String, nullable=False)

    def to_response(self):
        return {
            "pigeon_id": self.pigeon_id,
            "private_key": self.private_key,
            "public_key": self.public_key,
        }

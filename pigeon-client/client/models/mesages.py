from datetime import datetime
from . import db
from enum import  Enum, auto
from sqlalchemy import create_engine, Column, Integer, String, DateTime

class Message(db):
    __tablename__ = 'messages'

    mid = Column(Integer, primary_key=True)
    # cid = Column(String(80), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    sender = Column(String(80), nullable=False)
    recipient = Column(String(80), nullable=False)
    message = Column(String(300), nullable=False)

    def to_dict(self):
        return {
        # 'cid': self.cid,
        'mid': self.mid,
        'created_at': self.created_at.strftime("%Y-%m-%dT%H:%M:%SZ") if self.created_at else None,
        'contents': {
            'to': self.recipient,
            'from': self.sender,
            'message': self.message,
        },
        }

    def __repr__(self):
        return f'<Message {self.mid} {self.sender} {self.message}>'

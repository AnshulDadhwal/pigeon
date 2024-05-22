from datetime import datetime
from . import db
from enum import  Enum, auto
from sqlalchemy import create_engine, Column, Integer, String

# class Chat(db.Model):
class Chat(db):
    __tablename__ = 'chats'

    cid = Column(String(80), primary_key=True)
    users = Column(String(80), default="[]",nullable=False)

    def get(self, var):
        if var =='cid':
            return self.cid
        if var =='sender':
            return self.sender
        if var =='receiver':
            return self.receiver
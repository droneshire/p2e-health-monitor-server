from marshmallow import Schema, fields
from sqlalchemy.sql import func

from database.connect import db


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    wallets = db.Column(db.Integer, nullable=False)
    health_id = db.Column(db.Integer, db.ForeignKey("health.id"))
    last_ping = db.Column(db.DateTime(timezone=True), server_default=func.now())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}:{self.id} {self.wallets}>"


class UserSchema(Schema):  # type: ignore
    id = fields.Int()
    username = fields.Str()
    wallets = fields.Int()
    health_id = fields.Int()
    last_ping = fields.DateTime()
    created_at = fields.DateTime()

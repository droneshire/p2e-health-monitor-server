from marshmallow import Schema, fields
from sqlalchemy.sql import func

from database.connect import db
from database.user import UserSchema


class Health(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    num_users = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", backref="health")
    last_ping = db.Column(db.DateTime(timezone=True), server_default=func.now())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Health {self.name}>"


class HealthSchema(Schema):  # type: ignore
    id = fields.Int()
    name = fields.Str()
    num_users = fields.Int()
    last_ping = fields.DateTime()
    users = fields.List(fields.Nested(UserSchema))
    created_at = fields.DateTime()

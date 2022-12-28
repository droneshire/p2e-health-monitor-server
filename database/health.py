from sqlalchemy.sql import func

from database.connect import db


class Health(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    alive = db.Column(db.Integer, nullable=False)
    num_users = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", backref="health")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Health {self.name}>"

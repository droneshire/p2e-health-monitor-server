from sqlalchemy.sql import func

from database.connect import db


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    wallets = db.Column(db.Integer, nullable=False)
    config_update = db.Column(db.DateTime(timezone=True), server_default=func.now())
    health_id = db.Column(db.Integer, db.ForeignKey("health.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username} {self.wallets}>"

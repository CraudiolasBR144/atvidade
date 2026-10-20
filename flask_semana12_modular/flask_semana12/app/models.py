from datetime import datetime
from zoneinfo import ZoneInfo

from app import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.name!r}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")),
        nullable=False,
    )

    def __repr__(self):
        return f"<User {self.username!r}>"


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")),
        nullable=False,
    )

    def __repr__(self):
        return f"<Email {self.id}: {self.recipient!r}>"

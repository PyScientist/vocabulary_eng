from typing import Optional
from datetime import datetime, timezone
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from hashlib import md5


@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))


class Users(UserMixin, db.Model):

    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=False)
    nickname: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    words: so.WriteOnlyMapped['Words'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return 'Users {}'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Words(db.Model):

    __tablename__ = 'words'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False)
    speach_part: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=False)
    translations: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False)
    definition: so.Mapped[str] = so.mapped_column(sa.String(300), unique=False)
    importance: so.Mapped[str] = so.mapped_column(sa.Integer(), index=True, unique=False)
    topic: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=False)
    creation_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Users.id), index=True, unique=False)
    author: so.Mapped[Users] = so.relationship(back_populates='words')

    def __repr__(self):
        return 'Words {}'.format(self.name)
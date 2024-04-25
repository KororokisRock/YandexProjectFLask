from flask_login import UserMixin

from .db_session import SqlAlchemyBase

import sqlalchemy
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('status.id'))
    status = orm.relationship('Status')
    jobs = orm.relationship('Job', back_populates='user')
    command_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('commands.id'))
    command = orm.relationship('Command')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

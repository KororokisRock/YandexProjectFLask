from .db_session import SqlAlchemyBase

import sqlalchemy
from sqlalchemy import orm

from sqlalchemy_serializer import SerializerMixin


class Command(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'commands'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    users = orm.relationship('User', back_populates='command')

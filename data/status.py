from .db_session import SqlAlchemyBase

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Status(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'status'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    level_redact_profile = sqlalchemy.Column(sqlalchemy.Integer)
    level_job = sqlalchemy.Column(sqlalchemy.Integer)
    users = orm.relationship('User', back_populates='status')

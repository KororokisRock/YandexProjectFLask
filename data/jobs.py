from .db_session import SqlAlchemyBase

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.String)
    end_date = sqlalchemy.Column(sqlalchemy.String)
    complete = sqlalchemy.Column(sqlalchemy.Boolean)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')

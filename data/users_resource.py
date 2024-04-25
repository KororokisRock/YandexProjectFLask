from flask_restful import Resource
from flask_restful import reqparse

from flask_login import current_user

from flask import abort
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import redirect

from . import db_session

from .user import User
from .status import Status
from .command import Command

from forms.user import UserRedactLowLevelForm
from forms.user import UserRedactHightLevelForm
from forms.user import UserDeleteAccountForm


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        form = UserDeleteAccountForm()
        status = user.status
        command = user.command
        current_user_status = current_user.status
        db_sess.close()
        return make_response(render_template('user.html', user=user, status=status, current_user_status=current_user_status, command=command, form=form))

    def post(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/register')


parser_form_low_level = reqparse.RequestParser()
parser_form_low_level.add_argument('name', required=True, location='form')
parser_form_low_level.add_argument('description', required=True, location='form')
parser_form_low_level.add_argument('email', required=True, location='form')

parser_form_hight_level = reqparse.RequestParser()
parser_form_hight_level.add_argument('name', required=True, location='form')
parser_form_hight_level.add_argument('description', required=True, location='form')
parser_form_hight_level.add_argument('email', required=True, location='form')
parser_form_hight_level.add_argument('command_id', required=True, location='form')
parser_form_hight_level.add_argument('status_id', required=True, location='form')


class UserListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        users = [(user, user.status) for user in users if user.command_id == current_user.command_id]
        db_sess.close()
        return make_response(render_template('users.html', users=users))


class UserRedactResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)

        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)

        if current_user.id == user.id and current_user.status.id != -1:
            form = UserRedactLowLevelForm()
            form = [(form.name, user.name), (form.description, user.description),
                    (form.email, user.email), (form.submit, 0)]
        else:
            form = UserRedactHightLevelForm()
            form.command_id.choices = [(command.id, command.name) for command in db_sess.query(Command).all()]
            form.status_id.choices = [(status.id, status.name) for status in db_sess.query(Status).all()]
            form = [(form.name, user.name), (form.description, user.description),
                    (form.email, user.email), (form.command_id, user.command_id), (form.status_id, user.status_id),  (form.submit, 0)]

        db_sess.close()
        return make_response(render_template('user_redact.html', form=form, user=user))

    def post(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)

        if current_user.id == user.id and current_user.status.id != -1:
            args = parser_form_low_level.parse_args()
            user.name = args['name']
            user.description = args['description']
            user.email = args['email']
        else:
            args = parser_form_hight_level.parse_args()
            user.name = args['name']
            user.description = args['description']
            user.email = args['email']
            user.command_id = args['command_id']
            user.status_id = args['status_id']
        db_sess.commit()
        db_sess.close()

        return redirect(f'/api/v2/users/{user_id}')

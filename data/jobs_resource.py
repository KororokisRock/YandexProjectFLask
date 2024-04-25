from flask_restful import Resource
from flask_restful import reqparse

from flask_login import current_user

from flask import abort
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import redirect

from . import db_session

from .jobs import Job

from forms.user import JobCloseForm
from forms.user import JobCreateForm


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Job).get(job_id)
    if not jobs:
        abort(404)


class JobResource(Resource):
    def get(self, job_id):
        form = JobCloseForm()
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Job).get(job_id)
        user = jobs.user
        if (user.command_id == current_user.command_id and user.status.level_job < current_user.status.level_job) or current_user.status.id == -1:
            session.close()
            return make_response(render_template('job_moder.html', job=jobs, forms=form, user=user))
        elif jobs.user_id == current_user.id:
            session.close()
            return make_response(render_template('job_view.html', job=jobs, user=user))
        else:
            session.close()
            return make_response(render_template('not_pass.html'))

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        session.delete(job)
        session.commit()
        session.close()
        return redirect('/register')

    def post(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        session.delete(job)
        session.commit()
        session.close()
        return redirect('/api/v2/jobs')


parser_form = reqparse.RequestParser()
parser_form.add_argument('title', required=True, location='form')
parser_form.add_argument('description', required=True, location='form')
parser_form.add_argument('start_date', required=True, location='form')
parser_form.add_argument('end_date', required=True, location='form')
parser_form.add_argument('user_id', required=True, type=int, location='form')


class JobListResource(Resource):
    def get(self):
        session = db_session.create_session()
        current_user_status = current_user.status
        jobs = session.query(Job).all()
        jobs = [(job, job.user) for job in jobs if job.user_id == current_user.id or (job.user.command_id == current_user.command_id and job.user.status.level_job < current_user.status.level_job)
                or (job.user.command_id == current_user.command_id and current_user.status.id == -1)]
        session.close()
        return make_response(render_template('jobs.html', jobs=jobs, current_user_status=current_user_status))


class JobCreateResource(Resource):
    def get(self):
        form = JobCreateForm()
        form.user_id.choices = [(user.id, f'{user.name} - {user.id}') for user in current_user.command.users
                                    if (user.status.level_job < current_user.status.level_job and user.status.id != -1) or current_user.status.id == -1]
        return make_response(render_template('job_create.html', forms=form))

    def post(self):
        args = parser_form.parse_args()
        session = db_session.create_session()
        job = Job(
            title=args['title'],
            description=args['description'],
            user_id=args['user_id'],
            complete=False,
            start_date=args['start_date'],
            end_date=args['end_date']
        )
        session.add(job)
        session.commit()
        session.close()
        return redirect('/api/v2/jobs')

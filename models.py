# For more details, see
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping
from anthill.framework.db import db


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    repo_url = db.Column(db.String(512), nullable=False)
    repo_branch = db.Column(db.String(128), default='master')
    repo_ssh_key = db.Column(db.Text)
    versions = db.relationship(
        'ApplicationVersion', backref='application', lazy='dynamic',
        cascade='all, delete-orphan')


class ApplicationVersion(db.Model):
    __tablename__ = 'application_versions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(128), nullable=False)
    commit = db.Column(db.String(128), nullable=False, unique=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey('applications.id'), nullable=False, index=True)

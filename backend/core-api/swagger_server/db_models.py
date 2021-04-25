from swagger_server.app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # personal data
    email = db.Column(db.String(128), index=True)
    first_name = db.Column(db.String(128), index=True)
    family_name = db.Column(db.String(128), index=True)
    role = db.Column(db.String(128), index=True)

    # service data
    key = db.Column(db.LargeBinary)
    salt = db.Column(db.LargeBinary)
    recovery_key = db.Column(db.LargeBinary)
    recovery_status = db.Column(db.Integer, default=0)
    log_out = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Patient(db.Model):
    id = db.Column(db.String(128), primary_key=True)

    name = db.Column(db.String(128))

    studies = db.relationship('Study', backref='patient', lazy='selectin')


class Instance(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    order = db.Column(db.Integer())
    preview = db.Column(db.Text())

    series_id = db.Column(db.String(128), db.ForeignKey('series.id'))


class Series(db.Model):
    id = db.Column(db.String(128), primary_key=True)

    study_id = db.Column(db.String(128), db.ForeignKey('study.id'))

    instances = db.relationship('Instance', backref='series', lazy='selectin', order_by="Instance.order")

    orientation = db.Column(db.String(128))

    original_state = db.Column(db.JSON())
    dynamic_state = db.Column(db.JSON())


class Study(db.Model):
    id = db.Column(db.String(128), primary_key=True)

    patient_id = db.Column(db.String(128), db.ForeignKey('patient.id'))

    series = db.relationship('Series', backref='study', lazy='selectin')

    date = db.Column(db.DateTime)

    description = db.Column(db.String(128))

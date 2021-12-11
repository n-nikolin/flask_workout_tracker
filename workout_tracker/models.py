from . import db
# TODO: this is a prototype that will later be rewritten in django
# don't overwhelm yourself or spend too much time on it


class Programme(db.Model):
    __tableneame__ = 'programme'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    programme_name = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_started = db.Column(db.DateTime, nullable=True)
    date_finished = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
    programme_workouts = db.relationship(
        'Workout', backref='programme', lazy=True)


class Workout(db.Model):
    __tableneame__ = 'workout'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    workout_name = db.Column(db.String(60), nullable=False)
    programme_id = db.Column(db.Integer, db.ForeignKey(
        'programme.id'), nullable=False)
    workout_exercises = db.relationship(
        'Exercise', backref='workout', lazy=True)


class Exercise(db.Model):
    __tableneame__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    exercise_name = db.Column(db.String(60), nullable=False)
    num_sets = db.Column(db.Integer, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey(
        'workout.id'), nullable=False)
    exercise_sets = db.relationship('Set', backref='exercise', lazy=True)


class Set(db.Model):
    __tableneame__ = 'set'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(10, 2), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Numeric(10, 2), nullable=True)
    reps = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercise.id'), nullable=False)

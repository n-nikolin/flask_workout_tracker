from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from werkzeug.exceptions import BadRequest

from . import db
from .models import Programme, Workout, Exercise, Set

"""
REFACTORING, ADDING BASIC FUNCTIONALITY AND MAKING CODE MORE CONCISE:
    TODO: refactor routes and make them more compact
    TODO: put error handlers into separate file
    TODO: add update_programme feature
ADD FEATURES
    TODO: connect to an auth api
    TODO: add user logs
    TODO: add auto-increment feature
LOOK INTOS:
    TODO: to make less db calls look into rewriting models
    to optimise queries
"""

main = Blueprint('main', __name__)


def get_programme_workouts(output, programme):
    # loops through queried data and makes it json serializable
    workouts = Workout.query.filter_by(programme_id=programme.id).all()
    for workout in workouts:
        exercises = Exercise.query.filter_by(workout_id=workout.id).all()
        workout_list = output[-1]["workouts"]
        workout_list.append(
            {"workout_name": workout.workout_name, "exercises": []})

        for exercise in exercises:
            sets = Set.query.filter_by(exercise_id=exercise.id).all()
            exercise_list = workout_list[-1]['exercises']
            exercise_list.append(
                {"exercise_name": exercise.exercise_name, 'sets': []})

            for set in sets:
                set_list = exercise_list[-1]['sets']
                set_list.append({
                    "set_order": set.order,
                    "weight": set.weight,
                    'duration': set.duration,
                    'reps': set.reps,
                    'distance': set.distance
                })
    return output


@main.route('/api/create_programme', methods=['GET', 'POST'])
def create_programme():
    # loops through incoming json data and inserts objects into a database
    # handles bad requests
    if BadRequest:
        message = 'Inconsistent data'
        return jsonify(message=message)

    data = request.get_json()
    try:
        new_programme = Programme(
            programme_name=data['programme_name'],
            date_created=datetime.now()
        )
        db.session.add(new_programme)
        db.session.commit()

        for workout_data in data['workouts']:
            new_workout = Workout(
                workout_name=workout_data['workout_name'],
                programme_id=new_programme.id
            )
            db.session.add(new_workout)
            db.session.commit()

            for exercise_data in workout_data['exercises']:
                new_exercise = Exercise(
                    exercise_name=exercise_data['exercise_name'],
                    workout_id=new_workout.id
                )
                db.session.add(new_exercise)
                db.session.commit()

                for set_data in exercise_data['sets']:
                    
                    counter = 0
                    for i in set_data.items():
                        if i == None:
                            counter+=1
                    if counter >= 3:
                        # message = 'cannot create empty set'
                        raise KeyError

                    new_set = Set(
                        order=set_data['set_order'],
                        reps=set_data['reps'],
                        weight=set_data['weight'],
                        duration=set_data['duration'],
                        distance=set_data['distance'],
                        exercise_id=new_exercise.id
                    )
                    
                    db.session.add(new_set)
                db.session.commit()
        message = f'programme created! id = {new_programme.id}'

    # handles sql errors
    except exc.DataError:
        db.session.rollback()
        message = 'dataerror'
    
    # There were a couple of times when this was useful and worked and now it seems useless
    # Maybe test it out a few times and then delete
    # except KeyError:
    #     db.session.delete(new_programme)
    #     db.session.commit()
    #     message = f'inconsistent data! programme_id={new_programme.id} rejected'

    return jsonify({'message': message})


@main.route('/api/programmes', methods=['GET'])
def get_all_programmes():
    # outputs all programmes from db
    output = []
    programmes = Programme.query.all()
    for programme in programmes:
        output.append(
            {"programme_name": programme.programme_name,
             "workouts": []})
        get_programme_workouts(output, programme)
    return jsonify({"message": output})


@main.route('/api/programmes/<programme_id>', methods=['GET'])
def get_one_programme(programme_id):
    # outputs a single programme, based on id
    programme = Programme.query.filter_by(id=programme_id).first()
    if not programme:
        return jsonify(message=f'programme with id = {programme_id} does not exist')
    output = [{"programme_name": programme.programme_name, "workouts": []}]
    get_programme_workouts(output, programme)
    return jsonify({"message": output[0]})


@main.route('/api/programmes/<programme_id>/delete', methods=['DELETE'])
def delete_programme(programme_id):
    # deletes all programme objects, inclusing ones from related tables
    programme = Programme.query.filter_by(id=programme_id).first()
    db.session.delete(programme)
    db.session.commit()
    return jsonify({'message': f'programme has {programme.id} been deleted'})

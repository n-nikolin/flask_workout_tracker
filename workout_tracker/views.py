from datetime import datetime

from flask import Blueprint, request, jsonify

from . import db
from .models import Programme, Workout, Exercise, Set

main = Blueprint('main', __name__)


@main.route('/api/create_programme', methods=['GET', 'POST'])
def create_programme():
    data = request.get_json()
    # TODO: make it a loop?
    for obj in data.values():
        if obj == "":
            return jsonify({'message': "error, bitch!"}), 400

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
                num_sets=exercise_data['num_sets'],
                workout_id=new_workout.id
            )
            db.session.add(new_exercise)
            db.session.commit()

            for set_data in exercise_data['sets']:
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

    return jsonify({'message': "programme created"})


@main.route('/api/programmes', methods=['GET'])
def get_all_programmes():
    # TODO: find a way to make it less shit and optimize
    output = []
    programmes = Programme.query.all()

    for programme in programmes:
        workouts = Workout.query.filter_by(programme_id=programme.id).all()
        output.append(
            {"programme_name": programme.programme_name, "workouts": []})

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
                        'distace': set.distance
                    })
    return jsonify({"message": output})


@main.route('/api/programmes/<programmeId>', methods=['GET'])
def get_one_programme(programmeId):
    # TODO: rewrite this as separate function or some shit,
    # because it's almost the same as the get all programmes route
    programme = Programme.query.filter_by(id=programmeId).first()
    programme_data = {
        "programme_name": programme.programme_name, "workouts": []}
    workouts = Workout.query.filter_by(programme_id=programme.id).all()

    for workout in workouts:
        workout_list = programme_data['workouts']
        workout_list.append(
            {"workout_name": workout.workout_name, "exercises": []})
        exercises = Exercise.query.filter_by(workout_id=workout.id).all()
    
        for exercise in exercises:
            sets = Set.query.filter_by(exercise_id=exercise.id).all()
            exercise_list = workout_list[-1]['exercises']
            exercise_list.append(
                {"exercise_name": exercise.exercise_name, "sets": []})
    
            for set in sets:
                set_list = exercise_list[-1]["sets"]
                set_list.append({
                    'order': set.order,
                    "weight": set.weight,
                    'duration': set.duration,
                    'distance': set.distance,
                    'reps': set.reps
                })
    
    return jsonify({"message": programme_data})


@main.route('/api/<programe_id>/delete', methods=['DELETE'])
def delete_programme(programme_id):
    pass

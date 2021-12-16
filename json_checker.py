# write a script that checks json file for faulty data
# so that the incoming data is normalized
import json

set_data = {
    "set_order": 1,
    "weight": None,
    "duration": None,
    "distance": None,
    "reps": 5
}

def check_dict_data(my_dict):
    counter = 0
    for v in my_dict.values():
        if v == None:
            counter+=1
        print(v)
    if counter >= 3:
        print('pidr')
    print(my_dict)
    print(counter)

check_dict_data(set_data)

def check_json_data(json_file):
    input = json.loads(json_file.read())
    print(input.items())


# with open('pppp.json', 'r') as f_obj:
#     check_json_data(f_obj)

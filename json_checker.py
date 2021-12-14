# write a script that checks json file for faulty data
# so that the incoming data is normalized
import json

def check_json_data(json_file):
    input = json.loads(json_file.read())
    # print(type(input))
    if KeyError in input:
        print('penis')
    #     for j in i[::]:
    #         pass
    #         print(j)
    #         for k in i:
    #             print(k)
    # print(input)


with open('pppp.json', 'r') as f_obj:
    check_json_data(f_obj)

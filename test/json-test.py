import json

with open('/home/archie/Machine-Learning/Datasets/high-res.geo.json', 'r') as file:
    json_text = json.load(file)



print(json_text)
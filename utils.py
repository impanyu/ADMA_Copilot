import json

def is_json(myjson):
    try:
        result = json.loads(myjson)
    except ValueError as e:
        return False
    return result
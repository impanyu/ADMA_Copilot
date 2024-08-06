import json

def is_json(myjson):
    if myjson.startswith("```json") and myjson.endswith("```"):
        # Strip the first line (```json\n) and the last line (```)
        myjson = myjson.split('\n', 1)[1].rsplit('\n', 1)[0]
    try:
        result = json.loads(myjson)
    except ValueError as e:
        return False
    return result
import json
import sys


def string_to_json(response_str):
    try:
        return json.loads(response_str)
    except ValueError as error:
        print("JsonParsing Error: ", error, file=sys.stderr)

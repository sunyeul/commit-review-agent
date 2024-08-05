import json


def extract_and_parse_json(raw_string):
    # Find the JSON part within the string
    json_start = raw_string.find("{")
    json_end = raw_string.rfind("}") + 1
    json_content = raw_string[json_start:json_end]

    # Parse the JSON content
    parsed_json = json.loads(json_content)
    return parsed_json

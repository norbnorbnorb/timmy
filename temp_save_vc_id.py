import json
from pathlib import Path

temp_file_name = 'temp_ids.json'
temp_file = Path.cwd() / temp_file_name


def dump_to_json(data: dict, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


def read_json(file):
    with open(file, 'r') as f:
        data_dict = json.load(f)
    return data_dict


def delete_file(file):
    try:
        file.unlink()
    except OSError as e:
        print(f'Error: {file}, {e.strerror}')

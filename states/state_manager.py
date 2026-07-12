## IMPORTS ##

import json
import configparser
from pathlib import Path

## VARIABLES ##

script_dir = Path(__file__).resolve().parent

## PRIVATE FUNCTIONS ##



def _get_file_path(file_name: str,) -> Path:
    return script_dir / file_name ## "states/" -> "states/FILE_NAME+.FILE_EXTENSION"

def _delete_file(file_name: str):
     file_path = _get_file_path(file_name)
     file_path.unlink(missing_ok=True)

def _read_json_file(file_path: Path):
    data = {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass # juckt
    except Exception as err:
        print("Unexpected Error:", err)

    return data

def _edit_json_file(file_name: str, index: str, value) -> None:
    file_path = _get_file_path(file_name)
    json_data = _read_json_file(file_path)
    if json_data is not None:
        try:
            json_data[index] = value

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)

        except Exception as err:
            
            print("Fehler beim bearbeiten einer Datei:", err) # TODO: Zum Failure System anschließen
            pass


## PUBLIC FUNCTIONS ##

def edit_setting_state(section: str, key: str, value) -> bool:
    file_path = _get_file_path("settings.ini")
    settings_config = configparser.ConfigParser()

    settings_config.read(file_path, encoding="utf-8")
    if section not in settings_config:
        settings_config[section] = {}

    settings_config[section][key] = str(value)
    try:
        with open(file_path, "w", encoding="utf-8") as configfile:
            settings_config.write(configfile)
    except Exception as err:
        print("Error while trying to access settings.ini:", err) # TODO: Zum Failure System anschließen
        return False
    return True


def edit_ui_state(index: str, value) -> None:
    _edit_json_file("ui_state.json", index, value)

def reset_ui_state_file(file_name: str) -> None:
    file_path = _get_file_path(file_name)
    try:
        file_path.unlink(missing_ok=True)
    except Exception:
        pass
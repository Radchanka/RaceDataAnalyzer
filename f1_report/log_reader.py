from datetime import datetime
import os


def read_log_file(file_path: str) -> list[str]:
    """
    Reads the contents of a log file.

    Args:
        file_path (str): The path to the log file.

    Returns:
        list[str]: A list of lines from the log file.
    """
    filename = os.path.basename(file_path).lower()

    if filename in ["start.log", "end.log", "abbreviations.txt"]:
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read()
        return content.splitlines()
    else:
        raise ValueError("Unsupported file. Only 'start.log', 'end.log', and 'abbreviations.txt' are allowed.")


def read_race_data(folder_path: str) -> tuple[dict[str, datetime], dict[str, datetime]]:
    """
    Reads the race data from the given folder path.

    Args:
        folder_path (str): The path to the folder containing the data files.

    Returns:
        tuple[dict[str, datetime], dict[str, datetime]]: A tuple of start_times and end_times dictionaries.
    """
    start_times = {}
    end_times = {}

    start_lines = read_log_file(os.path.join(folder_path, "start.log"))
    end_lines = read_log_file(os.path.join(folder_path, "end.log"))

    for start_line, end_line in zip(start_lines, end_lines):
        start_initials = start_line[:3]
        start_time_str = start_line[3:].strip()
        start_times[start_initials] = datetime.strptime(start_time_str, "%Y-%m-%d_%H:%M:%S.%f")

        end_initials = end_line[:3]
        end_time_str = end_line[3:].strip()
        end_times[end_initials] = datetime.strptime(end_time_str, "%Y-%m-%d_%H:%M:%S.%f")

    return start_times, end_times


def read_abbreviations(folder_path: str) -> dict[str, dict[str, str]]:
    """
    Reads the abbreviations data from the given folder path.

    Args:
        folder_path (str): The path to the folder containing the abbreviations file.

    Returns:
        dict[str, dict[str, str]]: A dictionary of abbreviations with driver names and team names.
    """
    abbreviations = {}

    abbrev_lines = read_log_file(os.path.join(folder_path, "abbreviations.txt"))

    for line in abbrev_lines:
        initials, driver_name, team_name = line.strip().split("_")
        abbreviations[initials] = {"driver": driver_name, "team": team_name}

    return abbreviations

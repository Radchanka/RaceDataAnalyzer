from operator import itemgetter
from f1_report.log_reader import read_race_data, read_abbreviations
import datetime


def format_lap_time(lap_time: datetime.timedelta) -> str:
    hours = lap_time.seconds // 3600
    minutes = (lap_time.seconds // 60) % 60
    seconds = lap_time.seconds % 60
    milliseconds = lap_time.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def find_driver_by_name(abbreviations: dict, target_driver_name: str):
    if target_driver_name in abbreviations:
        return {target_driver_name: abbreviations[target_driver_name]}


def build_report(folder_path, target_driver_name=None, save_to_db_func=None):
    start_times, end_times = read_race_data(folder_path)
    abbreviations = read_abbreviations(folder_path)

    if target_driver_name:
        driver = find_driver_by_name(abbreviations, target_driver_name)
        if driver:
            abbreviations = driver
        else:
            raise ValueError(f"Driver '{target_driver_name}' not found!")

    best_laps = []
    invalid_laps = []

    for driver_initials, driver_info in abbreviations.items():
        driver_name = driver_info.get("driver", "Unknown")
        team_name = driver_info.get("team", "Unknown")

        if driver_initials in start_times and driver_initials in end_times:
            start_time = start_times[driver_initials]
            end_time = end_times[driver_initials]
            if start_time < end_time:
                lap_time = end_time - start_time
                lap_time_str = format_lap_time(lap_time)
                best_laps.append((driver_name, team_name, lap_time_str))
            else:
                invalid_laps.append((driver_name, team_name))

        if save_to_db_func:
            save_to_db_func(best_laps, invalid_laps)

    best_laps.sort(key=itemgetter(2))
    return best_laps, invalid_laps

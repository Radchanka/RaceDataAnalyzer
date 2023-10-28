from create_db import BestTable, InvalidTable
from f1_report.build_report import build_report


def save_data_to_db(best_laps, invalid_laps):
    for driver_name, team_name, lap_time_str in best_laps:
        lap_time_float = float(lap_time_str.replace(':', '').replace('.', ''))

        existing_record = BestTable.select().where(
            BestTable.driver_name == driver_name,
            BestTable.team_name == team_name,
            BestTable.lap_time == lap_time_float
        ).first()

        if not existing_record:
            BestTable.create(driver_name=driver_name, team_name=team_name, lap_time=lap_time_float)

    for driver_name, team_name in invalid_laps:
        existing_record = InvalidTable.select().where(
            InvalidTable.driver_name == driver_name,
            InvalidTable.team_name == team_name,
            InvalidTable.lap_time == 'Error'
        ).first()

        if not existing_record:
            InvalidTable.create(driver_name=driver_name, team_name=team_name, lap_time='Error')


if __name__ == "__main__":
    folder_path = 'data'
    best_laps, invalid_laps = build_report(folder_path, save_to_db_func=save_data_to_db)

from tabulate import tabulate
from f1_report.config import MAX_BEST_LAPS


def print_report(best_laps: list[tuple[str, str, str]], invalid_laps: list[tuple[str, str]]) -> None:
    headers = ["Pos.", "Driver", "Team", "Lap Time"]
    data = []

    for i, (driver, team, lap_time) in enumerate(best_laps[:MAX_BEST_LAPS], 1):
        data.append([f"{i:3d}.", driver, team, lap_time])

    max_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]

    data.append(["-" * length for length in max_lengths])

    for i, (driver, team, lap_time) in enumerate(best_laps[MAX_BEST_LAPS:], MAX_BEST_LAPS + 1):
        data.append([f"{i:3d}.", driver, team, lap_time])

    table = tabulate(data, headers, tablefmt="outline")
    print(table)

    if invalid_laps:
        invalid_headers = ["Driver", "Team", "Lap Time"]
        invalid_data = []
        for driver, team in invalid_laps:
            invalid_data.append([driver, team, 'ERROR'])
        invalid_table = tabulate(invalid_data, invalid_headers, tablefmt="outline")

        print("\nInvalid Data:")
        print(invalid_table)

import argparse
from operator import itemgetter

from f1_report.build_report import build_report
from f1_report.print_report import print_report


def create_parser():
    parser = argparse.ArgumentParser(description="Formula 1 Race Report CLI")
    parser.add_argument("--files", required=True, help="Path to the race data files")
    parser.add_argument("--driver", help="Driver name to filter the report")
    parser.add_argument("--asc", action="store_true", help="Sort laps in ascending order")
    parser.add_argument("--desc", action="store_true", help="Sort laps in descending order")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    folder_path = args.files
    driver_name = args.driver

    try:
        report = build_report(folder_path, driver_name)
    except ValueError as e:
        print(f"Error occurred: {e}")
        return
    except FileNotFoundError:
        print("Data file not found. Please check your file path and file name.")
        return

    if args.asc:
        report[0].sort(key=itemgetter(2))
    elif args.desc:
        report[0].sort(key=itemgetter(2), reverse=args.asc or args.desc)

    print_report(*report)


if __name__ == "__main__":
    main()

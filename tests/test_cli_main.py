import unittest
from unittest.mock import patch
from io import StringIO

from cli import main

start_data = (
    "SVF2018-05-24_12:02:58.917\n"
    "VBM2018-05-24_12:00:00.000\n"
    "CLS2018-05-24_12:09:41.921\n"
    "LHM2018-05-24_12:18:20.125\n"
)
end_data = (
    "SVF2018-05-24_12:04:03.332\n"
    "VBM2018-05-24_12:01:12.434\n"
    "CLS2018-05-24_12:10:54.750\n"
    "LHM2018-05-24_12:11:32.585\n"
)
abbreviations_data = (
    "SVF_Sebastian Vettel_FERRARI\n"
    "VBM_Valtteri Bottas_MERCEDES\n"
    "CLS_Charles Leclerc_SAUBER FERRARI\n"
    "LHM_Lewis Hamilton_MERCEDES\n"
)


class TestMainOutput(unittest.TestCase):

    def setUp(self):
        self.mock_read_log_file = patch('f1_report.log_reader.read_log_file', side_effect=[
            StringIO(start_data),
            StringIO(end_data),
            StringIO(abbreviations_data)
        ]).start()
        self.addCleanup(self.mock_read_log_file.stop)

    def run_main(self, argv):
        with patch('sys.argv', argv):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                return mock_stdout.getvalue().strip()

    def test_output_asc(self):
        argv = ['', '--files', 'path_to_folder', '--asc']

        expected_output = (
            '+--------+------------------+----------------+--------------+\n'
            '| Pos.   | Driver           | Team           | Lap Time     |\n'
            '+========+==================+================+==============+\n'
            '| 1.     | Sebastian Vettel | FERRARI        | 00:01:04.415 |\n'
            '| 2.     | Valtteri Bottas  | MERCEDES       | 00:01:12.434 |\n'
            '| 3.     | Charles Leclerc  | SAUBER FERRARI | 00:01:12.829 |\n'
            '| ----   | ---------------- | -------------- | ------------ |\n'
            '+--------+------------------+----------------+--------------+\n'
            '\n'
            'Invalid Data:\n'
            '+----------------+----------+------------+\n'
            '| Driver         | Team     | Lap Time   |\n'
            '+================+==========+============+\n'
            '| Lewis Hamilton | MERCEDES | ERROR      |\n'
            '+----------------+----------+------------+'
        )

        self.assertEqual(self.run_main(argv), expected_output)

    def test_output_desc(self):
        argv = ['', '--files', 'path_to_folder', '--desc']

        expected_output = (
            '+--------+------------------+----------------+--------------+\n'
            '| Pos.   | Driver           | Team           | Lap Time     |\n'
            '+========+==================+================+==============+\n'
            '| 1.     | Charles Leclerc  | SAUBER FERRARI | 00:01:12.829 |\n'
            '| 2.     | Valtteri Bottas  | MERCEDES       | 00:01:12.434 |\n'
            '| 3.     | Sebastian Vettel | FERRARI        | 00:01:04.415 |\n'
            '| ----   | ---------------- | -------------- | ------------ |\n'
            '+--------+------------------+----------------+--------------+\n'
            '\n'
            'Invalid Data:\n'
            '+----------------+----------+------------+\n'
            '| Driver         | Team     | Lap Time   |\n'
            '+================+==========+============+\n'
            '| Lewis Hamilton | MERCEDES | ERROR      |\n'
            '+----------------+----------+------------+'
        )

        self.assertEqual(self.run_main(argv), expected_output)

    def test_output_driver(self):
        argv = ['', '--files', 'path_to_folder', '--driver', 'Sebastian Vettel']

        expected_output = (
            '+--------+------------------+---------+--------------+\n'
            '| Pos.   | Driver           | Team    | Lap Time     |\n'
            '+========+==================+=========+==============+\n'
            '| 1.     | Sebastian Vettel | FERRARI | 00:01:04.415 |\n'
            '| ----   | ---------------- | ------- | ------------ |\n'
            '+--------+------------------+---------+--------------+'
        )

        self.assertEqual(self.run_main(argv), expected_output)

    def test_driver_not_found(self):
        argv = ['', '--files', 'path_to_folder', '--driver', 'Nonexistent Driver']

        expected_output = "Error occurred: Driver 'Nonexistent Driver' not found!"

        self.assertEqual(self.run_main(argv), expected_output)

    @patch('f1_report.log_reader.read_log_file', side_effect=FileNotFoundError)
    def test_invalid_file_path(self, mock_read_log_file):
        argv = ['', '--files', 'nonexistent_folder']

        expected_message = "Data file not found. Please check your file path and file name."

        self.assertIn(self.run_main(argv), expected_message)

    @patch('f1_report.print_report.MAX_BEST_LAPS', 2)
    def test_output_with_max_best_laps(self):
        argv = ['', '--files', 'path_to_folder']

        expected_output = (
            '+--------+------------------+----------------+--------------+\n'
            '| Pos.   | Driver           | Team           | Lap Time     |\n'
            '+========+==================+================+==============+\n'
            '| 1.     | Sebastian Vettel | FERRARI        | 00:01:04.415 |\n'
            '| 2.     | Valtteri Bottas  | MERCEDES       | 00:01:12.434 |\n'
            '| ----   | ---------------- | --------       | ------------ |\n'
            '| 3.     | Charles Leclerc  | SAUBER FERRARI | 00:01:12.829 |\n'
            '+--------+------------------+----------------+--------------+\n'
            '\n'
            'Invalid Data:\n'
            '+----------------+----------+------------+\n'
            '| Driver         | Team     | Lap Time   |\n'
            '+================+==========+============+\n'
            '| Lewis Hamilton | MERCEDES | ERROR      |\n'
            '+----------------+----------+------------+'
        )

        self.assertEqual(self.run_main(argv), expected_output)

    def test_print(self):
        argv = ['', '--files', 'path_to_folder']

        expected_output = (
            '+--------+------------------+----------------+--------------+\n'
            '| Pos.   | Driver           | Team           | Lap Time     |\n'
            '+========+==================+================+==============+\n'
            '| 1.     | Sebastian Vettel | FERRARI        | 00:01:04.415 |\n'
            '| 2.     | Valtteri Bottas  | MERCEDES       | 00:01:12.434 |\n'
            '| 3.     | Charles Leclerc  | SAUBER FERRARI | 00:01:12.829 |\n'
            '| ----   | ---------------- | -------------- | ------------ |\n'
            '+--------+------------------+----------------+--------------+\n'
            '\n'
            'Invalid Data:\n'
            '+----------------+----------+------------+\n'
            '| Driver         | Team     | Lap Time   |\n'
            '+================+==========+============+\n'
            '| Lewis Hamilton | MERCEDES | ERROR      |\n'
            '+----------------+----------+------------+'
        )
        self.assertEqual(self.run_main(argv), expected_output)


if __name__ == '__main__':
    unittest.main()

from flask import Flask, request, Response
import json
import xml.etree.ElementTree as ET
import sqlite3
from flasgger import Swagger
from pathlib import Path

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.json')

# Path to the SQLite database
db_path = Path('f1_report/data/race_data.db')


@app.route('/api/v1/report/', methods=['GET'])
def get_report():
    # Get the output format (json or xml) from the request parameter
    output_format = request.args.get('format', default='json', type=str)

    if output_format == 'json':
        # If JSON format is chosen

        # Establish a connection to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Retrieve best and invalid laps data from the database
        cursor.execute('SELECT driver_name, team_name, lap_time FROM besttable')
        best_laps = cursor.fetchall()

        cursor.execute('SELECT driver_name, team_name FROM invalidtable')
        invalid_laps = cursor.fetchall()

        conn.close()

        # Create a JSON response
        response_data = {
            "best_laps": best_laps,
            "invalid_laps": invalid_laps
        }
        return Response(json.dumps(response_data), content_type='application/json')

    elif output_format == 'xml':
        # If XML format is chosen

        # Establish a connection to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Retrieve best and invalid laps data from the database
        cursor.execute('SELECT driver_name, team_name, lap_time FROM besttable')
        best_laps = cursor.fetchall()

        cursor.execute('SELECT driver_name, team_name FROM invalidtable')
        invalid_laps = cursor.fetchall()

        conn.close()

        # Create an XML response
        root = ET.Element("report")
        best_laps_elem = ET.SubElement(root, "best_laps")
        invalid_laps_elem = ET.SubElement(root, "invalid_laps")

        for driver in best_laps:
            driver_elem = ET.SubElement(best_laps_elem, "driver")
            driver_elem.text = ", ".join(map(str, driver))

        for driver in invalid_laps:
            driver_elem = ET.SubElement(invalid_laps_elem, "driver")
            driver_elem.text = ", ".join(map(str, driver))

        response_data = ET.tostring(root, encoding='utf-8', method='xml')
        return Response(response_data, content_type='application/xml')

    else:
        return {"error": "Unsupported format"}, 400


if __name__ == '__main__':
    app.run(debug=True)

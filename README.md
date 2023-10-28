RaceDataAnalyzer README

RaceDataAnalyzer is a web service for analyzing and providing insights into Formula 1 race data, including best lap times and invalidated laps. It is built with Flask, offering data in both JSON and XML formats.

Key Features:
- Retrieve comprehensive data on the best laps achieved in Formula 1 races.
- Gain insights into laps invalidated during races, along with driver and team information.
- Select your preferred output format (JSON or XML).

Getting Started:

1. Clone the repository to your local machine:
   - `git clone https://github.com/Radchanka/RaceDataAnalyzer.git`

2. Install the required dependencies:
   - `pip install -r requirements.txt`

3. Launch the project:
   - `python app.py`

4. Open your web browser and navigate to `http://localhost:5000/api/v1/report/`. Add the `format` parameter to the URL with the value `json` or `xml` to obtain data in your preferred format.

API Documentation:
- The API documentation is accessible through Swagger UI. To explore supported endpoints and understand how to use the API effectively, visit `http://localhost:5000/apidocs/` in your web browser.

License:
- This project is distributed under the MIT License. For full details, please refer to the LICENSE file.

Author:
- Uladzimir Radchanka

Contact:
- For inquiries or suggestions related to the project, please feel free to contact us via email at URadchanka@gmail.com.

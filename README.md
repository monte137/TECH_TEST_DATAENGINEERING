# TECH_TEST_DATAENGINEERING
Solution to tech challenge

## Weather Data Extraction and Update
This Python script extracts weather data from the CONAGUA API, combines it with existing data from previous extractions, and saves the updated data to a CSV file.

### Requirements
The script requires the following Python packages:

* requests
* pandas
* os
* datetime

### Usage
To run the script, execute the main() function at the end of the file. The script will first attempt to extract new data from the CONAGUA API. If the extraction fails, it will instead read data from a JSON file "HourlyForecast_MX". It will then combine this new data with existing data located in the latest folder (based on its name in format YYYYMMDD) in the data_municipios directory. The updated data will be saved to a CSV file in the "output" directory with the current date and time as the file name. Additionally, a file named current.csv will be saved in the same directory with the most up-to-date data.

### Configuration
The script requires the following configuration:

The path to the main folder where the data and output directories are located should be set in the path variable in the main() function.
The get_weather_data() function uses a URL to connect to the CONAGUA API. This URL can be updated if the API endpoint changes.
"data_municipios" and "HourlyForecast_MX" folders should be download for the script to run correctly.

### Challenges faced
The main challenge I faced during this tech test was that I found the CONAGUA API wasn't working. That complicated the process at first, however the CONAGUA website still let me download the last dataframe available, which allowed me to develop the script. The first thing the script does is trying to connect to the API, in case this isn't possible, data is directly taken from the "HourlyForecast_MX".


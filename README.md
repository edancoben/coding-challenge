# coding-challenge

Hello!!

dependencies in "requirements.txt"

I left some commented out code in so you can see some extra steps in my thought process.
Hope it's helpful!


Problem 1:

-- models found in answers/api/models.py &
-- migrations found in answers/api/migrations
-- model names are WeatherData & model YieldData
-- comments in models.py file


Problem 2:

-- RUN "python manage.py ingest_data" or "python manage.py ingest_data --d"
-- d option deletes all rows in both db tables
-- code is found in answers/api/problem_2_ingestion.py & answers/api/management/commands/ingest_data.py 
-- unit tests in answers/api/tests/test_data_ingestion.py


Problem 3:

-- RUN "python manage.py analyze_weather" or "python manage.py analyze_weather --d"
-- d option deletes all rows in both db tables
-- code is found in answers/api/problem_3_analysis.py & answers/api/management/commands/analyze_weather.py
-- model WeatherAnalysis found in answers/api/models.py with comments
-- unit tests in answers/api/tests/test_data_analysis.py


Problem 4:

GET ENDPOINTS:
-- /api/weather
-- /api/yield
-- /api/weather/stats/ (need the slash at the end from my testing in postman for this specific route)

-- FILTERS: code is looking for query params "date" or "weather_station" or "year" where present

-- 100 records retured per page
-- can filter by date (ex: "1985-01-01") and weather_station (ex: "USC00110072") or year (ex: "2012") where present
-- code is found in answers/api/views.py
-- serializers in answers/api/serializers.py
-- unit tests in answers/api/tests/test_views.py

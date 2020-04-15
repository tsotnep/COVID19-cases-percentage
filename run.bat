Rem delete previously generated files
del "parsed_population.json" >nul 2>&1
del "parsed_cases.json" >nul 2>&1
del "plot1.png" >nul 2>&1
del "plot2.png" >nul 2>&1
del "plot3.png" >nul 2>&1

cd parser_worldometer/parser_worldometer
scrapy crawl parse_cases -o ../../parsed_cases.json
scrapy crawl parse_population -o ../../parsed_population.json

cd ../../analyze_data
python analyze1.py
python analyze2.py
python analyze3.py

Rem pause
Rem delete previously generated files
del "parsed_*.json" >nul 2>&1
del "img*.png" >nul 2>&1


Rem PARSE WEB
cd parser_web/parser_worldometer
scrapy crawl parse_cases -o ../../parsed_cases.json
scrapy crawl parse_population -o ../../parsed_population.json
python replaceNames.py
cd ../parser_githubCasesByDays
python webJsonToDataframes.py

Rem pause

cd ../../analyze_data
python analyze1.py
python analyze2.py
python analyze3.py
python analyze4.py
python analyze5.py
python analyze6.py 
python analyze7.py 
python analyze8.py 
python analyze9.py 
python analyze10.py 
python merge.py 
python merge2.py 
pause
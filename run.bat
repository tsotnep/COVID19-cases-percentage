Rem delete previously generated files
del "parsed_population.json" >nul 2>&1
del "parsed_cases.json" >nul 2>&1
del "img1_*.png" >nul 2>&1
del "img2_*.png" >nul 2>&1
del "img3_*.png" >nul 2>&1
del "img4_*.png" >nul 2>&1

cd parser_worldometer/parser_worldometer
scrapy crawl parse_cases -o ../../parsed_cases.json
scrapy crawl parse_population -o ../../parsed_population.json

cd ../../analyze_data
python analyze1.py
Rem python analyze2.py
python analyze3.py
python analyze4.py

Rem pause
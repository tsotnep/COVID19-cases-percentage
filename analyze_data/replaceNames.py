import fileinput

with fileinput.FileInput('../parsed_cases.json', inplace=True) as file:
    for line in file:
        print(line.replace("USA","US"), end='')

with fileinput.FileInput('../parsed_cases.json', inplace=True) as file:
    for line in file:
        print(line.replace("UK","United Kingdom"), end='')

with fileinput.FileInput('../parsed_cases.json', inplace=True) as file:
    for line in file:
        print(line.replace("UAE","United Arab Emirates"), end='')

with fileinput.FileInput('../parsed_cases.json', inplace=True) as file:
    for line in file:
        print(line.replace("S. Korea","Korea, South"), end='')



with fileinput.FileInput('../parsed_population.json', inplace=True) as file:
    for line in file:
        print(line.replace("United States","US"), end='')

with fileinput.FileInput('../parsed_population.json', inplace=True) as file:
    for line in file:
        print(line.replace("South Korea","Korea, South"), end='')
        
        
        
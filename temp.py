import csv
import json

def neoCounter():
    with open('./data/neos.csv', 'r') as file:
        reader = csv.DictReader(file)
        countName = 0
        countDiam = 0
        for neo in reader:
            if neo['name'] != '':
                print(neo['name'])
                countName += 1
            if neo['diameter'] != '':
                print(neo['diameter'])
                countDiam += 1
      
    print('total is ' + str(countName) + ' named.')
    print('total is ' + str(countDiam) + ' with a diameter.')

# neoCounter()

def cadProcessor():
    with open('./data/cad.json', 'r') as file:
        cadData = json.load(file)
        approachData = cadData['data']

    dateMatch = [approach for approach in approachData if approach[7].count('t')]
    for approach in dateMatch:
        print(approach)

cadProcessor()
import xlsxwriter
from datetime import date
import Upland.upland as upland
import os
import sys

headers = {'user-agent': 'HeatMap/1.1'}
homedir = os.path.expanduser('~')

searchCity = sys.argv[1]
tableData = {}

neighbourhoods = upland.getNeighbourhood(headers, searchCity)

for neighbourhood in neighbourhoods:
  tableData[neighbourhood['id']] = {'neighbourhood name': neighbourhood['name'], 'data':{'total properties': 0, 'non-fsa properties': 0, 'fsa properties': 0}}

for neighbourhoodID, details in tableData.items():
  props = upland.getNeighbourhoodProperties(headers, searchCity, details['neighbourhood name'])
  props = props[0]
  tableData[neighbourhoodID]['data']['total properties'] = len(props)
  for prop in props:
    try:
      if prop['labels']['fsa_allow']:
        tableData[neighbourhoodID]['data']['fsa properties'] += 1
      else:
        tableData[neighbourhoodID]['data']['non-fsa properties'] += 1
    except:
      print(prop)
today = date.today()
workbook = xlsxwriter.Workbook(homedir + '/maps/HeatmapData/' + searchCity + ' Pre-Release Data' + today.strftime('%d-%b') + '.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0

firstNeighbourhoodID = next(iter(tableData))
worksheet.write(row, col, 'neighbourhood name')

for columnHeader in tableData[firstNeighbourhoodID]['data']:
  col += 1
  worksheet.write(row, col, columnHeader)
row += 1

for neighbourhoodData in tableData.values():
  col = 0
  worksheet.write(row, col, neighbourhoodData['neighbourhood name'])
  for data in neighbourhoodData['data'].values():
    col += 1
    worksheet.write(row, col, data)
  row += 1

workbook.close()
    
            

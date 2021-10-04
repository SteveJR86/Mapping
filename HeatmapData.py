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
  if neighbourhood['boundaries']:
    tableData[neighbourhood['id']] = {'neighbourhood name': neighbourhood['name'], 'coordinates': neighbourhood['boundaries']['coordinates'][0], 'data':{'total properties': 0, 'total unlocked properties': 0, 'locked properties': 0, 'total minted': 0, 'owned properties': 0, 'non FSA unminted properties': 0, 'FSA unminted properties': 0, 'for sale properties': 0}}

for neighbourhoodID, details in tableData.items():
  props = upland.getNeighbourhoodProperties(headers, searchCity, details['neighbourhood name'])
  if props:
    props = props[0]
  tableData[neighbourhoodID]['data']['total properties'] = len(props)
  tableData[neighbourhoodID]['data']['total unlocked properties'] = len(props)
  for prop in props:
    if prop['status'] == 'Owned':
      tableData[neighbourhoodID]['data']['owned properties'] += 1
      tableData[neighbourhoodID]['data']['total minted'] += 1
    elif prop['status'] == 'For sale':
      tableData[neighbourhoodID]['data']['for sale properties'] += 1
      tableData[neighbourhoodID]['data']['total minted'] += 1
    elif prop['status'] == 'Unlocked':
      if prop['labels']['fsa_allow']:
        tableData[neighbourhoodID]['data']['FSA unminted properties'] += 1
      else:
        tableData[neighbourhoodID]['data']['non FSA unminted properties'] += 1
    elif prop['status'] == 'Locked':
      tableData[neighbourhoodID]['data']['locked properties'] += 1
      tableData[neighbourhoodID]['data']['total unlocked properties'] -= 1

today = date.today()
workbook = xlsxwriter.Workbook(homedir + '/maps/HeatmapData/' + searchCity + ' ' + today.strftime('%d-%b') + '.xlsx')
worksheet = workbook.add_worksheet()
percentage_format = workbook.add_format()
percentage_format.set_num_format('0.00%')
row = 0
col = 0

firstNeighbourhoodID = next(iter(tableData))
worksheet.write(row, col, 'neighbourhood name')

for columnHeader in tableData[firstNeighbourhoodID]['data']:
  col += 1
  worksheet.write(row, col, columnHeader)
  if not col == 1:
    col += 1
    worksheet.write(row, col, '% ' + columnHeader)
row += 1

for neighbourhoodData in tableData.values():
  col = 0
  worksheet.write(row, col, neighbourhoodData['neighbourhood name'])
  for data in neighbourhoodData['data'].values():
    col += 1
    worksheet.write(row, col, data)
    if not col == 1:
      col += 1
      if col < 6:
        worksheet.write(row, col, '=INDIRECT("R[0]C[-1]", FALSE())/INDIRECT("R[0]C[-' + str(col-1) + ']", FALSE() * 100)', percentage_format)
      else:
        worksheet.write(row, col, '=INDIRECT("R[0]C[-1]", FALSE())/INDIRECT("R[0]C[-' + str(col-2) + ']", FALSE() * 100)', percentage_format)
  row += 1

workbook.close()
    
            

import xlsxwriter
from datetime import date
import Upland.upland as upland
import os

headers = {'user-agent': 'HeatMap/1.1'}
homedir = os.path.expanduser('~')

searchCity = 'Kansas'
tableData = {}

neighbourhoods = upland.getNeighbourhood(headers, searchCity)

for neighbourhood in neighbourhoods:
  tableData[neighbourhood['id']] = {'neighbourhood_name': neighbourhood['name'], 'coordinates': neighbourhood['boundaries']['coordinates'][0], 'data':{'total_properties': 0, 'total_unlocked_properties': 0, 'total_minted': 0, 'owned_properties': 0, 'non_fsa_unminted_properties': 0, 'fsa_unminted_properties': 0, 'locked_properties': 0, 'for_sale_properties': 0}}

for neighbourhoodID, details in tableData.items():
  props = upland.getNeighbourhoodProperties(headers, searchCity, details['neighbourhood_name'])
  tableData[neighbourhoodID]['data']['total_properties'] = len(props)
  tableData[neighbourhoodID]['data']['total_unlocked_properties'] = len(props)
  for prop in props:
    if prop['status'] == 'Owned':
      tableData[neighbourhoodID]['data']['owned_properties'] += 1
      tableData[neighbourhoodID]['data']['total_minted'] += 1
    elif prop['status'] == 'For sale':
      tableData[neighbourhoodID]['data']['for_sale_properties'] += 1
      tableData[neighbourhoodID]['data']['total_minted'] += 1
    elif prop['status'] == 'Unlocked':
      if prop['labels']['fsa_allow']:
        tableData[neighbourhoodID]['data']['fsa_unminted_properties'] += 1
      else:
        tableData[neighbourhoodID]['data']['non_fsa_unminted_properties'] += 1
    elif prop['status'] == 'Locked':
      tableData[neighbourhoodID]['data']['locked_properties'] += 1
      tableData[neighbourhoodID]['data']['total_unlocked_properties'] -= 1

today = date.today()
workbook = xlsxwriter.Workbook(homedir + '/maps/HeatmapData/' + searchCity + ' ' + today.strftime('%d-%b') + '.xlsx')
worksheet = workbook.add_worksheet()
percentage_format = workbook.add_format()
percentage_format.set_num_format('0%')
row = 0
col = 0

firstNeighbourhoodID = next(iter(tableData))
worksheet.write(row, col, 'neighbourhood_name')

for columnHeader in tableData[firstNeighbourhoodID]['data']:
  col += 1
  worksheet.write(row, col, columnHeader)
  if not col == 1:
    col += 1
    worksheet.write(row, col, '% ' + columnHeader)
row += 1

for neighbourhoodData in tableData.values():
  col = 0
  worksheet.write(row, col, neighbourhoodData['neighbourhood_name'])
  for data in neighbourhoodData['data'].values():
    col += 1
    worksheet.write(row, col, data)
    if not col == 1:
      col += 1
      worksheet.write(row, col, '=INDIRECT("R[0]C[-1]", FALSE())/INDIRECT("R[0]C[-' + str(col-1) + ']", FALSE() * 100)', percentage_format)
  row += 1

workbook.close()
    
            

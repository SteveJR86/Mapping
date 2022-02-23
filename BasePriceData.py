import xlsxwriter
from datetime import date
import Upland.upland as upland
import os
import sys

def main():

  headers = {'user-agent': 'BasePrice/1.1'}
  homedir = os.path.expanduser('~')

  searchCity = sys.argv[1]
  tableData = {}

  neighbourhoods = upland.getNeighbourhood(headers, searchCity)

  for neighbourhood in neighbourhoods:
    tableData[neighbourhood['id']] = {'neighbourhood name': neighbourhood['name'], 'data':{'base price': 0}}

  for neighbourhoodID, details in tableData.items():
    props = upland.getNeighbourhoodProperties(headers, searchCity, details['neighbourhood name'])
    if not len(props) == 0:
      props = props[0]
      if not len(props) == 0:
        for prop in props:
          if not prop['status'] == 'Locked':
            break
        propDetails = upland.getPropertyDetails(headers, prop['prop_id'])
        tableData[neighbourhoodID]['data']['base price'] = calculateBasePrice(headers, propDetails)

  today = date.today()
  workbook = xlsxwriter.Workbook(homedir + '/maps/HeatmapData/' + searchCity + ' Base Prices.xlsx')
  worksheet = workbook.add_worksheet()
  percentage_format = workbook.add_format()
  percentage_format.set_num_format('0%')
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

  return
    
def calculateBasePrice(headers, prop):
  try:
    price = (prop['yield_per_hour']*59524)/prop['area']
  except:
    price = 0
  collectionLevels = []
  collections = upland.matchCollections(headers, prop['prop_id'])
  for collection in collections:
    if not collection == "King of the Street" and collection == "Newbie" and collection == "City Pro":
      collectionLevels.append(collection['category'])
  if collectionLevels:
    if max(collectionLevels) == 5:
      basePrice = price/21
    elif max(collectionLevels) == 4:
      basePrice = price/11
    elif max(collectionLevels) == 3:
      basePrice = price/3
    elif max(collectionLevels) == 2:
      basePrice = price/1.5
    else:
      basePrice = price
  else:
    basePrice = price
  return basePrice

if __name__ == '__main__':
  main()

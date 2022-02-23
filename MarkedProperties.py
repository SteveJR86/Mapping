import Upland.upland as upland
import Upland.plotting as plotting
import os
import sys
from datetime import date
import xlsxwriter

today = date.today()

homedir = os.path.expanduser('~')

headers = {'user-agent': 'PropertyMarkers/1.0'}

city = sys.argv[1]

neighbourhoods = upland.getNeighbourhood(headers, city)
neighbourhoodsProperties = upland.getNeighbourhoodProperties(headers, city)

workbook = xlsxwriter.Workbook(homedir + '/maps/MarkerData/' + city + ' ' + today.strftime('%d-%b') + '.xlsx')
worksheet = workbook.add_worksheet()
percentage_format = workbook.add_format()
percentage_format.set_num_format('0.00%')

worksheet.write(0, 0, 'Full Address')
worksheet.write(0, 1, 'Marked Property Name')

row = 1

for properties in neighbourhoodsProperties:
  for prop in properties:
    if prop['markers']:
      propDetails = upland.getPropertyDetails(headers, prop['prop_id'])
      worksheet.write(row, 0, propDetails['full_address'])
      try:
        worksheet.write(row, 1, prop['markers'][0]['title'])
        print(prop['markers'][0]['title'])
      except:
        print(prop)
      row += 1
  
workbook.close()

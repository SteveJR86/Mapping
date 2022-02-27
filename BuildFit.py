import Upland.upland as upland
import Upland.plotting as plotting
from shapely import affinity
import math
import xlsxwriter
import os

def main():
  headers = {'user-agent': 'buildfit/1.0'}
  neighbourhood = 'Avalon Park'
  city = 'Chicago'
  homedir = os.path.expanduser('~')
  workbook = xlsxwriter.Workbook(homedir + '/maps/BuildFitData/' + city + ' - ' + neighbourhood + '.xlsx')
  worksheet = workbook.add_worksheet()
  props = upland.getNeighbourhoodProperties(headers, city, neighbourhood)
  buildTypes = upland.getBuildings(headers, props[0][0]['prop_id'])
  worksheet.write(0, 0, 'Property Link')
  worksheet.write(0, 1, 'Full Address')
  worksheet.write(0, 2, 'Username')
  worksheet.write(0, 3, 'Is It Built?')
  col = 4
  for buildType in buildTypes:
    worksheet.write(0, col, buildType['buildingImage'].split("/")[0].replace("_", " ").replace(" new", "").replace("2", " 2"))
    col += 1
  col = 4
  row = 1
  for prop in props[0]:
    response, propDetails = upland.checkFit(headers, prop['prop_id'])
    worksheet.write(row, 0, f"https://play.upland.me/?prop_id={propDetails['prop_id']}")
    worksheet.write(row, 1, propDetails['full_address'])
    worksheet.write(row, 2, propDetails['owner_username'])
    try:
      worksheet.write(row, 3, propDetails['building']['constructionStatus'])
    except:
      pass
    for x, y in response.items():
      if y:
        worksheet.write(row, col, 'Fits')
      else:
        worksheet.write(row, col, 'Does Not Fit')
      col += 1
    row += 1
    col = 4
  workbook.close()

  return

if __name__ == '__main__':
  main()

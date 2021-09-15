import csv
import cairo
import json
import requests
import xlsxwriter
from shapely.geometry import Point
from shapely.geometry import Polygon
from datetime import date
from time import sleep

import Upland.upland as upland

def main():
  headers = {'user-agent': 'MapApp/1.1'}

  # parameters to set up depending on what is required:
  # Mode should be set to 1 for Neighbourhood plot, 2 for Area plot
  # and 3 for Street plot

  mapHeight = 3000
  propData = {}

  mode = 2
  users = {}
  users['Total'] = {}
  users['Total']['Total Properties'] = 0
  users['Total']['Total Owned Properties'] = 0
  users['Total']['FSA Unminted'] = 0
  users['Total']['Non-FSA Unminted'] = 0
  users['Total']['Owned By Others'] = 0
  users['Total']['For Sale'] = 0

  configFile = 'Superman Node - Bockioo1 - Sheet1.csv'
  filename = configFile[:-13]
  with open(configFile, newline='') as csvfile:
    configDetails = csv.reader(csvfile, delimiter=',')
      for num, row in enumerate(configDetails):
        if num == 0:
          pass
        elif num == 1:
          if not row[1] == '':
            searchProperties = list(map(int, row[1].split(', ')))
          if not row[3] == '':
            street = row[3]
        elif num == 2:
          neighbourhood = row[1]
          city = row[3]
        elif num > 3:
          if row[0] == 'Example Row':
            pass
          elif row[2] == 'Non-FSA Unminted':
            nonFSAColour = [int(row[3][1:3], 16)/255, int(row[3][3:5], 16)/255, int(row[3][5:7], 16)/255]
          elif row[2] == 'FSA Unminted':
            fsaColour = [int(row[3][1:3], 16)/255, int(row[3][3:5], 16)/255, int(row[3][5:7], 16)/255]
          elif row[2] == 'Owned by Others':
            ownedByOthers = [int(row[3][1:3], 16)/255, int(row[3][3:5], 16)/255, int(row[3][5:7], 16)/255]
          elif row[2] == 'For Sale by Others':
            forSaleColour = [int(row[3][1:3], 16)/255, int(row[3][3:5], 16)/255, int(row[3][5:7], 16)/255]
          elif not row[2] == '':
            username = row[2].lower()
            users[username] = {}
            users[username]['colour'] = [int(row[3][1:3], 16)/255, int(row[3][3:5], 16)/255, int(row[3][5:7], 16)/255]
            users[username]['data'] = {}
            users[username]['data']['Properties Owned'] = 0
            users[username]['data']['Total Up2'] = 0
            users[username]['data']['% of Group Ownership'] = 0
            users[username]['data']['% of Neighbourhood Ownership'] = 0
            users[username]['data']['Min Up2'] = None
            users[username]['data']['Max Up2'] = None
            users[username]['data']['Total Price Paid'] = 0
          else:
            break

  memberProperties = 0
  totalProperties = 0
  totalOwnedProperties = 0
  if mode == 1:
    properties = upland.getNeighbourhoodProperties(headers, city, neighbourhood)
    neighbourhoodPoly = upland.getNeighbourhoodPoly(headers, city, neighbourhood)
    props = properties[0]
  elif mode == 2 or mode == 3:
    propCoordinates = []
    for prop in searchProperties:
      propCoordinates.extend(json.loads(json.loads(requests.get('https://api.upland.me/properties/' + str(prop), headers=headers).text)['boundaries'])['coordinates'][0])
    neighbourhoodPoly = []
    neighbourhoodPoly.append(Polygon([
            (min(propCoordinates, key=lambda x: x[0])[0], min(propCoordinates, key=lambda x: x[1])[1]),
            (min(propCoordinates, key=lambda x: x[0])[0], max(propCoordinates, key=lambda x: x[1])[1]),
            (max(propCoordinates, key=lambda x: x[0])[0], max(propCoordinates, key=lambda x: x[1])[1]),
            (max(propCoordinates, key=lambda x: x[0])[0], min(propCoordinates, key=lambda x: x[1])[1])]))
    props = upland.getProperties(headers, neighbourhoodPoly[0])

  canvas2 = upland.makeCanvas(neighbourhoodPoly)
  surface = canvas2[0]
  canvas = canvas2[1]
  mapFactor = canvas2[2]
  upland.plotObject(canvas2[1], canvas2[2], neighbourhoodPoly, neighbourhoodPoly[0].bounds[0], neighbourhoodPoly[0].bounds[3])
  neighbourhoodPoly = neighbourhoodPoly[0]
  for prop in props:
    if mode == 3:
      propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
    coords = json.loads(prop['boundaries'])
    centrePoint = Point(float(prop['centerlng']), float(prop['centerlat']))
    if centrePoint.within(neighbourhoodPoly):
      if mode == 1 or mode == 2 or (mode == 3 and propDetails['full_address'].split(' ', 1)[1] == street.upper()):
        users['Total']['Total Properties'] += 1
        for num, point in enumerate(coords['coordinates'][0]):
          if num == len(coords['coordinates'][0]) - 1:
            break
          elif num == 0:
            canvas.move_to(((point[0] - neighbourhoodPoly.bounds[0]) * mapFactor), (mapHeight - (point[1] - neighbourhoodPoly.bounds[1]) * mapFactor))
          else:
            canvas.line_to(((point[0] - neighbourhoodPoly.bounds[0]) * mapFactor), (mapHeight - (point[1] - neighbourhoodPoly.bounds[1]) * mapFactor))
        if prop['status'] == 'Owned' :
          users['Total']['Total Owned Properties'] += 1
          if mode == 1 or mode ==2:
            try:
              propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
            except:
              sleep(1)
              propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
          if propDetails['owner_username'] in users:
            users[propDetails['owner_username']]['data']['Properties Owned'] += 1
            users[propDetails['owner_username']]['data']['Total Up2'] += propDetails['area']
            if users[propDetails['owner_username']]['data']['Min Up2'] == None:
              users[propDetails['owner_username']]['data']['Min Up2'] = propDetails['area']
            else:
              users[propDetails['owner_username']]['data']['Min Up2'] = min(users[propDetails['owner_username']]['data']['Min Up2'], propDetails['area'])
            if users[propDetails['owner_username']]['data']['Max Up2'] == None:
              users[propDetails['owner_username']]['data']['Max Up2'] = propDetails['area']
            else:
              users[propDetails['owner_username']]['data']['Max Up2'] = max(users[propDetails['owner_username']]['data']['Max Up2'], propDetails['area'])
            users[propDetails['owner_username']]['data']['Total Price Paid'] += propDetails['last_purchased_price']
            canvas.set_source_rgb(users[propDetails['owner_username']]['colour'][0], users[propDetails['owner_username']]['colour'][1], users[propDetails['owner_username']]['colour'][2])
          else:
            users['Total']['Owned By Others'] += 1
            canvas.set_source_rgb(ownedByOthers[0], ownedByOthers[1], ownedByOthers[2])
        elif prop['status'] == 'For sale':
          users['Total']['Total Owned Properties'] += 1
          if mode ==1 or mode == 2:
            propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
          if propDetails['owner_username'] in users:
            users[propDetails['owner_username']]['data']['Properties Owned'] += 1
            canvas.set_source_rgb(users[propDetails['owner_username']]['colour'][0], users[propDetails['owner_username']]['colour'][1], users[propDetails['owner_username']]['colour'][2])
          else:
            users['Total']['For Sale'] += 1
            canvas.set_source_rgb(forSaleColour[0], forSaleColour[1], forSaleColour[2])
        elif prop['status'] == "Unlocked" and prop['labels']['fsa_allow'] == True:
          users['Total']['FSA Unminted'] += 1
          canvas.set_source_rgb(fsaColour[0], fsaColour[1], fsaColour[2])
        elif prop['status'] == "Unlocked" and prop['labels']['fsa_allow'] == False:
          users['Total']['Non-FSA Unminted'] +=1
          canvas.set_source_rgb(nonFSAColour[0], nonFSAColour[1], nonFSAColour[2])
        else:
          canvas.set_source_rgb(0, 0, 0)
        canvas.close_path()
        canvas.fill_preserve()
        canvas.set_source_rgb(0, 0, 0)
        canvas.stroke()

  today = date.today()
  surface.write_to_png(filename + ' ' + today.strftime('%d-%b') + '.png')

  workbook = xlsxwriter.Workbook(filename + ' ' + today.strftime('%d-%b') + '.xlsx')
  worksheet = workbook.add_worksheet()
  row = 1
  col = 1
  columnFlag = True

  for user in users:
    if user != 'Total':
      users[user]['data']['% of Group Ownership'] = users[user]['data']['Properties Owned']/users['Total']['Total Owned Properties']
      users[user]['data']['% of Neighbourhood Ownership'] = users[user]['data']['Properties Owned']/users['Total']['Total Properties']
      if columnFlag:
        for num, field in enumerate(users[user]['data'], start=2):
          worksheet.write(0, num, field)
        columnFlag = False
       worksheet.write(row, col, user)
       for num, field in enumerate(users[user]['data']):
         worksheet.write(row, col + num + 1, users[user]['data'][field])
       row += 1
  row += 1

  for num, field in enumerate(users['Total']):
    worksheet.write(row, col + num + 1, field)
    worksheet.write(row + 1, col + num + 1, users['Total'][field])

  workbook.close()


if __name__ == '__main__':
  main()

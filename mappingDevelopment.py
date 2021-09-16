import csv
import os
import sys
from time import sleep
import cairo
import json
import requests
import xlsxwriter
from shapely.geometry import Point
from shapely.geometry import Polygon
from datetime import date
import Upland.upland as upland

def main():
  headers = {'user-agent': 'MapApp/1.1'}
  homedir = os.path.expanduser('~')

  mapHeight = 3000
  propData = {}
  neighbourhood = sys.argv[1]
  city = sys.argv[2]
##  neighbourhood = "midtown terrace"
##  city = "San Francisco"
  filename = homedir + '/maps/' + neighbourhood + " - " + city + " - Building Progress"

  props = upland.getNeighbourhoodProperties(headers, city, neighbourhood)
  neighbourhoodPoly = upland.getNeighbourhoodPoly(headers, city, neighbourhood)
  canvas2 = upland.makeCanvas(neighbourhoodPoly)
  surface = canvas2[0]
  canvas = canvas2[1]
  mapFactor = canvas2[2]
  minLat = canvas2[3]
  maxLong = canvas2[4]
  neighbourhoodPoly = neighbourhoodPoly[0]

  builtProps = 0
  inProgressProps = 0
  for prop in props:
    propBound = json.loads(prop['boundaries'])
    propPoly = Polygon(propBound['coordinates'][0])
    if prop['status'] == 'Owned':
      try:
        propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
      except:
        sleep(1)
        propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
      if propDetails['building'] == None:
        upland.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
      elif propDetails['building']['constructionStatus'] == 'completed':
        upland.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (0, 1, 0.15))
        builtProps += 1
      elif propDetails['building']['constructionStatus'] == 'processing' or propDetails['building']['constructionStatus'] == 'can-watch-ceremony':
        upland.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 0))
        inProgressProps += 1
    else:
      upland.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
  canvas.set_font_size(100)
  canvas.move_to(75, 75)
  canvas.show_text(f'{neighbourhood}, {city}: {(builtProps/len(props))*100:.0f}% Developed')
  today = date.today()
  surface.write_to_png(filename + ' ' + today.strftime('%d-%b') + '.png')

if __name__ == '__main__':
    main()

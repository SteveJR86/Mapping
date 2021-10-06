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
import Upland.plotting as plotting

def main():
  headers = {'user-agent': 'MapApp/1.1'}
  homedir = os.path.expanduser('~')

  mapHeight = 3000
  propData = {}
  neighbourhood = sys.argv[1]
  city = sys.argv[2]
##  neighbourhood = "alamo square"
##  city = "San Francisco"
  filename = homedir + '/maps/NeighbourhoodDevelopment/' + neighbourhood + " - " + city + " - Building Progress"
  models = True
  
  props = upland.getNeighbourhoodProperties(headers, city, neighbourhood, models)
  props = props[0]
  neighbourhoodPoly = upland.getNeighbourhoodPoly(headers, city, neighbourhood)
  canvas2 = plotting.makeCanvas(neighbourhoodPoly)
  surface = canvas2[0]
  canvas = canvas2[1]
  mapFactor = canvas2[2]
  minLat = canvas2[3]
  maxLong = canvas2[4]

  plotting.plotObject(canvas, mapFactor, neighbourhoodPoly[0], minLat, maxLong)

  builtProps = 0
  inProgressProps = 0
  score = 0
  for prop in props:
    propPoly = upland.makePoly(prop['boundaries'])
    if prop['status'] == 'Owned':      
      if len(prop['models']) == 0:
        plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
      elif prop['models'][0]['constructionStatus'] == 'completed':
        plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (0, 1, 0.15))
        builtProps += 1
        score += prop['models'][0]['options']['score']
      elif prop['models'][0]['constructionStatus'] == 'processing' or prop['models'][0]['constructionStatus'] == 'can-watch-ceremony':
        plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 0))
        inProgressProps += 1
        score += prop['models'][0]['options']['score']
    else:
      plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
  canvas.set_font_size(100)
  canvas.move_to(75, 75)
  canvas.show_text(f'{neighbourhood}, {city}: {(builtProps/len(props))*100:.0f}% Developed')
  canvas.move_to(75, 160)
  canvas.show_text(f'{builtProps} Completed, {inProgressProps} In Progress, "Score": {score}')
  today = date.today()
  surface.write_to_png(filename + ' ' + today.strftime('%d-%b') + '.png')

if __name__ == '__main__':
    main()

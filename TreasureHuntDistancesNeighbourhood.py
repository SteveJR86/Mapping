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
  filename = homedir + '/maps/TreasureHunt/Treasure Hunt Distances - ' + neighbourhood + " - " + city
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
    plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
  plotting.plotCircle(canvas, surface, mapFactor, 10000, minLat, maxLong, (0, 0, 0, 0.1))
  plotting.plotCircle(canvas, surface, mapFactor, 3000, minLat, maxLong, (0, 0, 0, 0.1))
  plotting.plotCircle(canvas, surface, mapFactor, 1000, minLat, maxLong, (0, 0, 0, 0.1))
  plotting.plotCircle(canvas, surface, mapFactor, 500, minLat, maxLong, (1, 0, 0, 0.4))
  plotting.plotCircle(canvas, surface, mapFactor, 200, minLat, maxLong, (1, 0, 0, 0.6))
  plotting.plotCircle(canvas, surface, mapFactor, 50, minLat, maxLong, (1, 0, 0, 0.8))
  canvas.set_font_size(100)
  canvas.move_to(75, 75)
  canvas.show_text(f'{neighbourhood}, {city}')
  today = date.today()
  surface.write_to_png(filename + ' ' + today.strftime('%d-%b') + '.png')

if __name__ == '__main__':
    main()

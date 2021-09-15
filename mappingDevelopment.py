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
import upland.upland as upland

def main():
  headers = {'user-agent': 'MapApp/1.1'}
  homedir = os.path.expanduser('~')
  # parameters to set up depending on what is required:
  # Mode should be set to 1 for Neighbourhood plot, 2 for Area plot
  # and 3 for Street plot

  mapHeight = 3000
  propData = {}
##  neighbourhood = sys.argv[1]
##  city = sys.argv[2]
  neighbourhood = "midtown terrace"
  city = "San Franscisco"
  filename = homedir + '/maps/' + neighbourhood + " - " + city + " - Building Progress"

  properties = upland.getNeighbourhoodProperties(headers, city, neighbourhood)
  neighbourhoodPoly = upland.getNeighbourhoodPoly(headers, city, neighbourhood)
  props = properties[0]

  canvas2 = upland.makeCanvas(neighbourhoodPoly)
  surface = canvas2[0]
  canvas = canvas2[1]
  mapFactor = canvas2[2]
  minLat = canvas2[3]
  minLong = canvas2[4]
  neighbourhoodPoly = neighbourhoodPoly[0]
  
  for prop in props:
    coords = json.loads(prop['boundaries'])
    centrePoint = Point(float(prop['centerlng']), float(prop['centerlat']))
    if centrePoint.within(neighbourhoodPoly):
      for num, point in enumerate(coords['coordinates'][0]):
        if num == len(coords['coordinates'][0]) - 1:
          break
        if num == 0:
          canvas.move_to(((point[0] - neighbourhoodPoly.bounds[0]) * mapFactor), (mapHeight - (point[1] - neighbourhoodPoly.bounds[1]) * mapFactor))
        else:
          canvas.line_to(((point[0] - neighbourhoodPoly.bounds[0]) * mapFactor), (mapHeight - (point[1] - neighbourhoodPoly.bounds[1]) * mapFactor))
      if prop['status'] == 'Owned':
        try:
          propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
        except:
          sleep(1)
          propDetails = json.loads(requests.get('https://api.upland.me/properties/' + str(prop['prop_id']), headers=headers).text)
        if propDetails['building'] == None:
          canvas.set_source_rgb(1, 1, 1)
        elif propDetails['building']['constructionStatus'] == 'completed':
          canvas.set_source_rgb(0, 1, 0.15)
        elif propDetails['building']['constructionStatus'] == 'processing' or propDetails['building']['constructionStatus'] == 'can-watch-ceremony':
          canvas.set_source_rgb(1, 1, 0)
      else:
        canvas.set_source_rgb(1, 1, 1)
      canvas.close_path()
      canvas.fill_preserve()
      canvas.set_source_rgb(0, 0, 0)
      canvas.stroke()

  today = date.today()
  surface.write_to_png(filename + ' ' + today.strftime('%d-%b') + '.png')

if __name__ == '__main__':
    main()

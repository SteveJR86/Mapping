import Upland.upland as upland
import os
import sys
from datetime import date


homedir = os.path.expanduser('~')

headers = {'user-agent': 'HeatMaps/1.0'}

city = sys.argv[1]

neighbourhoodsProperties = upland.getNeighbourhoodProperties(headers, city)

fillColours = []

for properties in neighbourhoodsProperties:
  properties[:] = [x for x in properties if not x['status'] == "Locked"]
  propsUndeveloped = 0
  for prop in properties:
    if prop['models'] == []:
      propsUndeveloped += 1
  try:
    percentUndeveloped = propsUndeveloped/len(properties)
  except:
    percentUndeveloped = None

  if percentUndeveloped == None:
    fillColours.append((1, 1, 1))
  elif percentUndeveloped >= 0.98:
    fillColours.append((0, 1, 0.364705882352941))
  elif percentUndeveloped >= 0.96 and percentUndeveloped < 0.98:
    fillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
  elif percentUndeveloped >= 0.94 and percentUndeveloped < 0.96:
    fillColours.append((0.56078431372549, 0.866666666666667, 0))
  elif percentUndeveloped >= 0.92 and percentUndeveloped < 0.94:
    fillColours.append((0.674509803921569, 0.792156862745098, 0))
  elif percentUndeveloped >= 0.90 and percentUndeveloped < 0.92:
    fillColours.append((0.764705882352941, 0.713725490196079, 0))
  elif percentUndeveloped >= 0.88 and percentUndeveloped < 0.90:
    fillColours.append((0.83921568627451, 0.627450980392157, 0))
  elif percentUndeveloped >= 0.86 and percentUndeveloped < 0.88:
    fillColours.append((0.901960784313726, 0.529411764705882, 0))
  elif percentUndeveloped >= 0.84 and percentUndeveloped < 0.86:
    fillColours.append((0.949019607843137, 0.419607843137255, 0))
  elif percentUndeveloped >= 0.82 and percentUndeveloped < 0.84:
    fillColours.append((0.984313725490196, 0.282352941176471, 0))
  elif percentUndeveloped > 0.80 and percentUndeveloped < 0.82:
    fillColours.append((1, 0, 0))
  elif percentUndeveloped <= 0.80:
    fillColours.append((0, 0, 0))
  else:
    fillColours.append((0, 0, 0))

neighbourhoodPolys = upland.getNeighbourhoodPoly(headers, city)

data = upland.makeCanvas(neighbourhoodPolys)
surface = data[0]
canvas = data[1]
mapFactor = data[2]
minLat = data[3]
maxLong = data[4]

canvas.set_line_width(4)

for num, neighbourhoodPoly in enumerate(neighbourhoodPolys):
  upland.plotObject(canvas, mapFactor, neighbourhoodPoly, minLat, maxLong, fillColours[num])

today = date.today()
canvas.set_source_rgb(0, 0, 0)
canvas.set_font_size(100)
canvas.move_to(75, 75)
canvas.show_text(city)
surface.write_to_png(homedir + '/maps/DevelopmentHeatmaps/' + city + ' ' + today.strftime('%d-%b') + '.png')

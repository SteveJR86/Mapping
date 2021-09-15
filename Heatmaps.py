import upland
import os
from datetime import date

homedir = os.path.expanduser('~')

headers = {'user-agent': 'HeatMaps/1.0'}

city = ('Kansas')

neighbourhoodsProperties = upland.getNeighbourhoodProperties(headers, city)

fillColours = []

for properties in neighbourhoodsProperties:
  properties[:] = [x for x in properties if not x['status'] == "Locked"]
  propsUnlocked = 0
  for prop in properties:
    if prop['status'] == "Unlocked":
      propsUnlocked += 1
  try:
    percentUnsold = propsUnlocked/len(properties)
  except:
    percentUnsold = None

  if percentUnsold == None:
    fillColours.append((1, 1, 1))
  elif percentUnsold >= 0.9:
    fillColours.append((0, 1, 0))
  elif percentUnsold >= 0.8 and percentUnsold < 0.9:
    fillColours.append((0.2, 1, 0))
  elif percentUnsold >= 0.7 and percentUnsold < 0.8:
    fillColours.append((0.4, 1, 0))
  elif percentUnsold >= 0.6 and percentUnsold < 0.7:
    fillColours.append((0.6, 1, 0))
  elif percentUnsold >= 0.5 and percentUnsold < 0.6:
    fillColours.append((0.8, 1, 0))
  elif percentUnsold >= 0.4 and percentUnsold < 0.5:
    fillColours.append((1, 1, 0))
  elif percentUnsold >= 0.3 and percentUnsold < 0.4:
    fillColours.append((1, 0.8, 0))
  elif percentUnsold >= 0.2 and percentUnsold < 0.3:
    fillColours.append((1, 0.6, 0))
  elif percentUnsold >= 0.1 and percentUnsold < 0.2:
    fillColours.append((1, 0.4, 0))
  elif percentUnsold > 0 and percentUnsold < 0.1:
    fillColours.append((1, 0, 0))
  elif percentUnsold == 0:
    fillColours.append((0, 0, 0))
  else:
    fillColours.append((0, 0, 0))

nonFsaFillColours = []

for properties in neighbourhoodsProperties:
  propsUnlocked = 0
  totalProps = 0
  for prop in properties:
    if prop['status'] == "Unlocked" and prop['labels']['fsa_allow']  == False:
      propsUnlocked += 1
    if prop['labels']['fsa_allow'] == False:
      totalProps += 1

  try:
    percentUnsold = propsUnlocked/totalProps
  except:
    percentUnsold = None

  if percentUnsold == None:
    nonFsaFillColours.append((1, 1, 1))
  elif percentUnsold >= 0.9:
    nonFsaFillColours.append((0, 1, 0))
  elif percentUnsold >= 0.8 and percentUnsold < 0.9:
    nonFsaFillColours.append((0.2, 1, 0))
  elif percentUnsold >= 0.7 and percentUnsold < 0.8:
    nonFsaFillColours.append((0.4, 1, 0))
  elif percentUnsold >= 0.6 and percentUnsold < 0.7:
    nonFsaFillColours.append((0.6, 1, 0))
  elif percentUnsold >= 0.5 and percentUnsold < 0.6:
    nonFsaFillColours.append((0.8, 1, 0))
  elif percentUnsold >= 0.4 and percentUnsold < 0.5:
    nonFsaFillColours.append((1, 1, 0))
  elif percentUnsold >= 0.3 and percentUnsold < 0.4:
    nonFsaFillColours.append((1, 0.8, 0))
  elif percentUnsold >= 0.2 and percentUnsold < 0.3:
    nonFsaFillColours.append((1, 0.6, 0))
  elif percentUnsold >= 0.1 and percentUnsold < 0.2:
    nonFsaFillColours.append((1, 0.4, 0))
  elif percentUnsold > 0 and percentUnsold < 0.1:
    nonFsaFillColours.append((1, 0, 0))
  elif percentUnsold == 0:
    nonFsaFillColours.append((0, 0, 0))
  else:
    nonFsaFillColours.append((0, 0, 0))
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
surface.write_to_png(homedir + '/maps/' + city + ' ' + today.strftime('%d-%b') + '.png')

data = upland.makeCanvas(neighbourhoodPolys)
surface = data[0]
canvas = data[1]
mapFactor = data[2]
minLat = data[3]
maxLong = data[4]

canvas.set_line_width(4)

for num, neighbourhoodPoly in enumerate(neighbourhoodPolys):
  upland.plotObject(canvas, mapFactor, neighbourhoodPoly, minLat, maxLong, nonFsaFillColours[num])

today = date.today()
canvas.set_source_rgb(0, 0, 0)
canvas.set_font_size(100)
canvas.move_to(75, 75)
canvas.show_text(city + ' (Non-FSA Only)')
surface.write_to_png(homedir + '/maps/' + city + ' Non-FSA ' + today.strftime('%d-%b') + '.png')

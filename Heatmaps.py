import Upland.upland as upland
import Upland.plotting as plotting
import os
import sys
from datetime import date


homedir = os.path.expanduser('~')

headers = {'user-agent': 'HeatMaps/2.0'}

city = sys.argv[1]

keyPositions = {
  "San Francisco": "BottomRight",
  "Manhatten": "BottomRight",
  "Brooklyn": "BottomRight",
  "Fresno": "BottomRight",
  "Oakland": "BottomRight",
  "Staten Island": "BottomRight",
  "Bakersfield": "BottomRight",
  "Chicago": "BottomLeft",
  "Cleveland": "TopLeft",
  "Santa Clara": "TopRight",
  "Kansas": "BottomLeft",
  "Rutherford": "BottomLeft",
  "New Orleans": "BottomRight"
  }

neighbourhoodsProperties = upland.getNeighbourhoodProperties(headers, city)

fillColours = []
cbfillColours = []

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
    cbfillColours.append((1, 1, 1))
  elif percentUnsold >= 0.9:
    fillColours.append((0, 1, 0.364705882352941))
    cbfillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif percentUnsold >= 0.8 and percentUnsold < 0.9:
    fillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    cbfillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif percentUnsold >= 0.6 and percentUnsold < 0.8:
    fillColours.append((0.56078431372549, 0.866666666666667, 0))
    cbfillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif percentUnsold >= 0.4 and percentUnsold < 0.6:
    fillColours.append((0.764705882352941, 0.713725490196079, 0))
    cbfillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif percentUnsold >= 0.2 and percentUnsold < 0.4:
    fillColours.append((0.901960784313726, 0.529411764705882, 0))
    cbfillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif percentUnsold >= 0.1 and percentUnsold < 0.2:
    fillColours.append((0.984313725490196, 0.282352941176471, 0))
    cbfillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif percentUnsold > 0 and percentUnsold < 0.1:
    fillColours.append((1, 0, 0))
    cbfillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif percentUnsold == 0:
    fillColours.append((0, 0, 0))
    cbfillColours.append((0, 0, 0))
  else:
    fillColours.append((0, 0, 0))
    cbfillColours.append((0, 0, 0))

nonFsaFillColours = []
cbnonFsaFillColours = []

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
    cbnonFsaFillColours.append((1, 1, 1))
  elif percentUnsold >= 0.9:
    nonFsaFillColours.append((0, 1, 0.364705882352941))
    cbnonFsaFillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif percentUnsold >= 0.8 and percentUnsold < 0.9:
    nonFsaFillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    cbnonFsaFillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif percentUnsold >= 0.6 and percentUnsold < 0.8:
    nonFsaFillColours.append((0.56078431372549, 0.866666666666667, 0))
    cbnonFsaFillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif percentUnsold >= 0.4 and percentUnsold < 0.6:
    nonFsaFillColours.append((0.764705882352941, 0.713725490196079, 0))
    cbnonFsaFillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif percentUnsold >= 0.2 and percentUnsold < 0.4:
    nonFsaFillColours.append((0.901960784313726, 0.529411764705882, 0))
    cbnonFsaFillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif percentUnsold >= 0.1 and percentUnsold < 0.2:
    nonFsaFillColours.append((0.984313725490196, 0.282352941176471, 0))
    cbnonFsaFillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif percentUnsold > 0 and percentUnsold < 0.1:
    nonFsaFillColours.append((1, 0, 0))
    cbnonFsaFillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif percentUnsold == 0:
    nonFsaFillColours.append((0, 0, 0))
    cbnonFsaFillColours.append((0, 0, 0))
  else:
    nonFsaFillColours.append((0, 0, 0))
    cbnonFsaFillColours.append((0, 0, 0))
neighbourhoodPolys = upland.getNeighbourhoodPoly(headers, city)

surface = []
canvas = []
mapFactor = []
minLat = []
maxLong = []

for x in range(4):
  data = plotting.makeCanvas(neighbourhoodPolys)
  surface.append(data[0])
  canvas.append(data[1])
  mapFactor.append(data[2])
  minLat.append(data[3])
  maxLong.append(data[4])
  canvas[x].set_line_width(4)

for num, neighbourhoodPoly in enumerate(neighbourhoodPolys):
  plotting.plotObject(canvas[0], mapFactor[0], neighbourhoodPoly, minLat[0], maxLong[0], fillColours[num])
  plotting.plotObject(canvas[1], mapFactor[1], neighbourhoodPoly, minLat[1], maxLong[1], cbfillColours[num])
  plotting.plotObject(canvas[2], mapFactor[2], neighbourhoodPoly, minLat[2], maxLong[2], nonFsaFillColours[num])
  plotting.plotObject(canvas[3], mapFactor[3], neighbourhoodPoly, minLat[3], maxLong[3], cbnonFsaFillColours[num])
  
today = date.today()

for x in range(4):
  if (x % 2) == 0:
    keyFile = "Heatmap-key.png"
  else:
    keyFile = "CBHeatmap-key.png"
  plotting.plotKey(canvas[x], surface[x], keyFile, keyPositions[city])
  canvas[x].set_source_rgb(0, 0, 0)
  canvas[x].set_font_size(100)
  canvas[x].move_to(75, 75)


  
canvas[0].show_text(city)
surface[0].write_to_png(homedir + '/maps/Heatmaps/' + city + ' ' + today.strftime('%d-%b') + '.png')
canvas[1].show_text(city)
surface[1].write_to_png(homedir + '/maps/Heatmaps/' + city + ' Wong Colour Scheme ' + today.strftime('%d-%b') + '.png')
canvas[2].show_text(city + ' (Non-FSA Only)')
surface[2].write_to_png(homedir + '/maps/Heatmaps/' + city + ' Non-FSA ' + today.strftime('%d-%b') + '.png')
canvas[3].show_text(city + ' (Non-FSA Only)')
surface[3].write_to_png(homedir + '/maps/Heatmaps/' + city + ' Non-FSA Wong Colour Scheme ' + today.strftime('%d-%b') + '.png')

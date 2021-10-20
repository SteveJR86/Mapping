import Upland.upland as upland
import Upland.plotting as plotting
import os
import sys
from datetime import date

## should program in functionality to also produce maps by total property count
## and by score

homedir = os.path.expanduser('~')

headers = {'user-agent': 'HeatMaps/1.0'}

city = sys.argv[1]

keyPositions = {
  "San Francisco": "TopLeft",
  "Manhattan": "BottomRight",
  "Brooklyn": "BottomRight",
  "Fresno": "TopRight",
  "Oakland": "BottomLeft",
  "Staten Island": "BottomRight",
  "Bakersfield": "BottomRight",
  "Chicago": "BottomLeft",
  "Cleveland": "TopLeft",
  "Santa Clara": "TopRight",
  "Kansas": "BottomLeft",
  "Rutherford": "BottomLeft",
  "New Orleans": "BottomRight"
  }

neighbourhoodsProperties = upland.getNeighbourhoodProperties(headers, city,None,True)

fillColours = []
cbfillColours = []
pdfillColours = []
pdcbfillColours = []
dsfillColours = []
dscbfillColours = []

for properties in neighbourhoodsProperties:
  properties[:] = [x for x in properties if not x['status'] == "Locked"]
  propsDeveloped = 0
  devScore = 0
  for prop in properties:
    if not len(prop['models']) == 0:
      propsDeveloped += 1
      try:
        devScore += prop['models'][0]['options']['score']
      except:
        pass
      
  print(propsDeveloped, devScore)
  try:
    percentDeveloped = propsDeveloped/len(properties)
  except:
    percentDeveloped = None

  if percentDeveloped == None:
    fillColours.append((1, 1, 1))
    cbfillColours.append((1, 1, 1))
  elif percentDeveloped <= 0.035:
    fillColours.append((0, 1, 0.364705882352941))
    cbfillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif percentDeveloped <= 0.07 and percentDeveloped > 0.035:
    fillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    cbfillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif percentDeveloped <= 0.105 and percentDeveloped > 0.07:
    fillColours.append((0.56078431372549, 0.866666666666667, 0))
    cbfillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif percentDeveloped <= 0.14 and percentDeveloped > 0.105:
    fillColours.append((0.764705882352941, 0.713725490196079, 0))
    cbfillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif percentDeveloped <= 0.175 and percentDeveloped > 0.14:
    fillColours.append((0.901960784313726, 0.529411764705882, 0))
    cbfillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif percentDeveloped <= 0.21 and percentDeveloped > 0.175:
    fillColours.append((0.984313725490196, 0.282352941176471, 0))
    cbfillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif percentDeveloped <= 0.25 and percentDeveloped > 0.21:
    fillColours.append((1, 0, 0))
    cbfillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif percentDeveloped >= 0.25:
    fillColours.append((0, 0, 0))
    cbfillColours.append((0, 0, 0))
  else:
    fillColours.append((0, 0, 0))
    cbfillColours.append((0, 0, 0))

  if propsDeveloped == None:
    pdfillColours.append((1, 1, 1))
    pdcbfillColours.append((1, 1, 1))
  elif propsDeveloped <= 5:
    pdfillColours.append((0, 1, 0.364705882352941))
    pdcbfillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif propsDeveloped <= 20 and propsDeveloped > 5:
    pdfillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    pdcbfillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif propsDeveloped <= 60 and propsDeveloped > 20:
    pdfillColours.append((0.56078431372549, 0.866666666666667, 0))
    pdcbfillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif propsDeveloped <= 100 and propsDeveloped > 60:
    pdfillColours.append((0.764705882352941, 0.713725490196079, 0))
    pdcbfillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif propsDeveloped <= 200 and propsDeveloped > 100:
    pdfillColours.append((0.901960784313726, 0.529411764705882, 0))
    pdcbfillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif propsDeveloped <= 400 and propsDeveloped > 200:
    pdfillColours.append((0.984313725490196, 0.282352941176471, 0))
    pdcbfillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif propsDeveloped <= 600 and propsDeveloped > 400:
    pdfillColours.append((1, 0, 0))
    pdcbfillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif propsDeveloped >= 600:
    pdfillColours.append((0, 0, 0))
    pdcbfillColours.append((0, 0, 0))
  else:
    pdfillColours.append((0, 0, 0))
    pdcbfillColours.append((0, 0, 0))

  if devScore == None:
    dsfillColours.append((1, 1, 1))
    dscbfillColours.append((1, 1, 1))
  elif devScore <= 20:
    dsfillColours.append((0, 1, 0.364705882352941))
    dscbfillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif devScore <= 250 and devScore > 20:
    dsfillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    dscbfillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif devScore <= 500 and devScore > 250:
    dsfillColours.append((0.56078431372549, 0.866666666666667, 0))
    dscbfillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif devScore <= 750 and devScore > 500:
    dsfillColours.append((0.764705882352941, 0.713725490196079, 0))
    dscbfillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif devScore <= 1000 and devScore > 750:
    dsfillColours.append((0.901960784313726, 0.529411764705882, 0))
    dscbfillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif devScore <= 2000 and devScore > 1000:
    dsfillColours.append((0.984313725490196, 0.282352941176471, 0))
    dscbfillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif devScore <= 3000 and devScore > 2000:
    dsfillColours.append((1, 0, 0))
    dscbfillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif devScore >= 3000:
    dsfillColours.append((0, 0, 0))
    dscbfillColours.append((0, 0, 0))
  else:
    dsfillColours.append((0, 0, 0))
    dscbfillColours.append((0, 0, 0))

neighbourhoodPolys = upland.getNeighbourhoodPoly(headers, city)

surface = []
canvas = []
mapFactor = []
minLat = []
maxLong = []

for x in range(6):
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
  plotting.plotObject(canvas[2], mapFactor[2], neighbourhoodPoly, minLat[2], maxLong[2], pdfillColours[num])
  plotting.plotObject(canvas[3], mapFactor[3], neighbourhoodPoly, minLat[3], maxLong[3], pdcbfillColours[num])
  plotting.plotObject(canvas[4], mapFactor[4], neighbourhoodPoly, minLat[4], maxLong[4], dsfillColours[num])
  plotting.plotObject(canvas[5], mapFactor[5], neighbourhoodPoly, minLat[5], maxLong[5], dscbfillColours[num])

keyFile = ["DevHeatmap-key.png",
           "CBDevHeatmap-key.png",
           "pdDevHeatmap-key.png",
           "pdCBDevHeatmap-key.png",
           "dsDevHeatmap-key.png",
           "dsCBDevHeatmap-key.png"]
           

for x in range(6):
  plotting.plotKey(canvas[x], surface[x], keyFile[x], keyPositions[city])
  canvas[x].set_source_rgb(0, 0, 0)
  canvas[x].set_font_size(100)
  canvas[x].move_to(75, 75)

today = date.today()

canvas[0].show_text('% Developed - ' + city)
surface[0].write_to_png(homedir + '/maps/DevelopmentHeatmaps/Development ' + city + ' ' + today.strftime('%d-%b') + '.png')
canvas[1].show_text('% Developed - ' + city)
surface[1].write_to_png(homedir + '/maps/DevelopmentHeatmaps/Development ' + city + ' Wong Colour Scheme ' + today.strftime('%d-%b') + '.png')
canvas[2].show_text('No. of Properties Developed - ' + city)
surface[2].write_to_png(homedir + '/maps/DevelopmentHeatmaps/Development no of props ' + city + ' ' + today.strftime('%d-%b') + '.png')
canvas[3].show_text('No. of Properties Developed - ' + city)
surface[3].write_to_png(homedir + '/maps/DevelopmentHeatmaps/Development no of props ' + city + ' Wong Colour Scheme ' + today.strftime('%d-%b') + '.png')
canvas[4].show_text('Property Development Score - ' + city)
surface[4].write_to_png(homedir + '/maps/DevelopmentHeatmaps/Development property development score ' + city + ' ' + today.strftime('%d-%b') + '.png')
canvas[5].show_text('Property Development Score - ' + city)
surface[5].write_to_png(homedir + '/maps/DevelopmentHeatmaps/Development property development score ' + city + ' Wong Colour Scheme ' + today.strftime('%d-%b') + '.png')

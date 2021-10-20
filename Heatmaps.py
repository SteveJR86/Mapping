import Upland.upland as upland
import Upland.plotting as plotting
import os
import sys
from datetime import date
import xlsxwriter

today = date.today()

homedir = os.path.expanduser('~')

headers = {'user-agent': 'LovelyMaps/1.0'}

city = sys.argv[1]

keyPositions = {
  "San Francisco": "TopLeft",
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

neighbourhoods = upland.getNeighbourhood(headers, city)
neighbourhoodsProperties = upland.getNeighbourhoodProperties(headers, city)

workbook = xlsxwriter.Workbook(homedir + '/maps/HeatmapData/' + city + ' ' + today.strftime('%d-%b') + '.xlsx')
worksheet = workbook.add_worksheet()
percentage_format = workbook.add_format()
percentage_format.set_num_format('0.00%')

worksheet.write(0, 0, 'Neighbourhood Name')
worksheet.write(0, 1, 'Total Properties')
worksheet.write(0, 2, 'All Unlocked Properties')
worksheet.write(0, 3, 'All Minted Properties')
worksheet.write(0, 4, 'All % Minted')
worksheet.write(0, 5, 'Non-FSA Properties')
worksheet.write(0, 6, 'Non-FSA Minted Properties')
worksheet.write(0, 7, 'Non-FSA % Minted')

for row, neighbourhood in enumerate(neighbourhoods, start=1):
  worksheet.write(row, 0, neighbourhood['name'])

fillColours = []
cbfillColours = []
nonFsaFillColours = []
cbnonFsaFillColours = []

totalProps = 0
totalPropsUnlocked = 0
totalPropsMinted = 0
totalNonFSAProps = 0
totalNonFSAPropsMinted = 0

for row, properties in enumerate(neighbourhoodsProperties, start=1):
  propsUnlocked = 0
  propsMinted = 0
  nonFSAProps = 0
  nonFSAPropsMinted = 0
  for prop in properties:
    totalProps += 1
    if prop['status'] == 'Owned' or prop['status'] == 'For sale':
      propsUnlocked += 1
      propsMinted += 1
      totalPropsUnlocked += 1
      totalPropsMinted += 1
      if prop['labels']['fsa_allow'] == False:
        nonFSAProps += 1
        nonFSAPropsMinted += 1
        totalNonFSAProps += 1
        totalNonFSAPropsMinted += 1
    if prop['status'] == 'Unlocked':
      propsUnlocked += 1
      totalPropsUnlocked += 1
      if prop['labels']['fsa_allow'] == False:
        nonFSAProps += 1
        totalNonFSAProps += 1
  try:
    percentSold = propsMinted/propsUnlocked
  except:
    percentSold = None

  try:
    percentNonFSASold = nonFSAPropsMinted/nonFSAProps
  except:
    percentNonFSASold = None

  worksheet.write(row, 1, len(properties))
  worksheet.write(row, 2, propsUnlocked)
  worksheet.write(row, 3, propsMinted)
  try:
    worksheet.write(row, 4, propsMinted/propsUnlocked, percentage_format)
  except:
    worksheet.write(row, 4, '-', percentage_format)
  worksheet.write(row, 5, nonFSAProps)
  worksheet.write(row, 6, nonFSAPropsMinted)
  try:
    worksheet.write(row, 7, nonFSAPropsMinted/nonFSAProps, percentage_format)
  except:
    worksheet.write(row, 7, '-', percentage_format)

  if percentSold == None:
    fillColours.append((1, 1, 1))
    cbfillColours.append((1, 1, 1))
  elif percentSold <= 0.1:
    fillColours.append((0, 1, 0.364705882352941))
    cbfillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif percentSold <= 0.2 and percentSold > 0.1:
    fillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    cbfillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif percentSold <= 0.4 and percentSold > 0.2:
    fillColours.append((0.56078431372549, 0.866666666666667, 0))
    cbfillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif percentSold <= 0.6 and percentSold > 0.4:
    fillColours.append((0.764705882352941, 0.713725490196079, 0))
    cbfillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif percentSold <= 0.8 and percentSold > 0.6:
    fillColours.append((0.901960784313726, 0.529411764705882, 0))
    cbfillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif percentSold <= 0.9 and percentSold > 0.8:
    fillColours.append((0.984313725490196, 0.282352941176471, 0))
    cbfillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif percentSold < 1 and percentSold > 0.9:
    fillColours.append((1, 0, 0))
    cbfillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif percentSold == 1:
    fillColours.append((0, 0, 0))
    cbfillColours.append((0, 0, 0))
  else:
    fillColours.append((0, 0, 0))
    cbfillColours.append((0, 0, 0))

  if percentNonFSASold == None:
    nonFsaFillColours.append((1, 1, 1))
    cbnonFsaFillColours.append((1, 1, 1))
  elif percentNonFSASold <= 0.1:
    nonFsaFillColours.append((0, 1, 0.364705882352941))
    cbnonFsaFillColours.append((0.901960784313726, 0.623529411764706, 0))
  elif percentNonFSASold <= 0.2 and percentNonFSASold > 0.1:
    nonFsaFillColours.append((0.411764705882353, 0.933333333333333, 0.137254901960784))
    cbnonFsaFillColours.append((0.337254901960784, 0.705882352941177, 0.913725490196078))
  elif percentNonFSASold <= 0.4 and percentNonFSASold > 0.2:
    nonFsaFillColours.append((0.56078431372549, 0.866666666666667, 0))
    cbnonFsaFillColours.append((0, 0.619607843137255, 0.450980392156863))
  elif percentNonFSASold <= 0.6 and percentNonFSASold > 0.4:
    nonFsaFillColours.append((0.764705882352941, 0.713725490196079, 0))
    cbnonFsaFillColours.append((0.941176470588235, 0.894117647058824, 0.258823529411765))
  elif percentNonFSASold <= 0.8 and percentNonFSASold > 0.6:
    nonFsaFillColours.append((0.901960784313726, 0.529411764705882, 0))
    cbnonFsaFillColours.append((0, 0.447058823529412, 0.698039215686275))
  elif percentNonFSASold <= 0.9 and percentNonFSASold > 0.8:
    nonFsaFillColours.append((0.984313725490196, 0.282352941176471, 0))
    cbnonFsaFillColours.append((0.835294117647059, 0.368627450980392, 0))
  elif percentNonFSASold < 1 and percentNonFSASold > 0.9:
    nonFsaFillColours.append((1, 0, 0))
    cbnonFsaFillColours.append((0.8, 0.474509803921569, 0.654901960784314))
  elif percentNonFSASold == 1:
    nonFsaFillColours.append((0, 0, 0))
    cbnonFsaFillColours.append((0, 0, 0))
  else:
    nonFsaFillColours.append((0, 0, 0))
    cbnonFsaFillColours.append((0, 0, 0))

worksheet.write(len(neighbourhoodsProperties)+2, 0, 'Totals')    
worksheet.write(len(neighbourhoodsProperties)+2, 1, totalProps)
worksheet.write(len(neighbourhoodsProperties)+2, 2, totalPropsUnlocked)
worksheet.write(len(neighbourhoodsProperties)+2, 3, totalPropsMinted)
try:
  worksheet.write(len(neighbourhoodsProperties)+2, 4, totalPropsMinted/totalPropsUnlocked, percentage_format)
except:
  worksheet.write(len(neighbourhoodsProperties)+2, 4, '-', percentage_format)
worksheet.write(len(neighbourhoodsProperties)+2, 5, totalNonFSAProps)
worksheet.write(len(neighbourhoodsProperties)+2, 6, totalNonFSAPropsMinted)
try:
  worksheet.write(len(neighbourhoodsProperties)+2, 7, totalNonFSAPropsMinted/totalNonFSAProps, percentage_format)
except:
  worksheet.write(len(neighbourhoodsProperties)+2, 7, '-', percentage_format)

workbook.close()

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

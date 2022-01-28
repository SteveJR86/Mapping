import os
import sys
from datetime import date
import Upland.upland as upland
import Upland.plotting as plotting
import re

def main():
  headers = {'user-agent': 'MapApp/1.1'}
  homedir = os.path.expanduser('~')

  mapHeight = 3000
  propData = {}
  neighbourhood = sys.argv[1]
  city = sys.argv[2]
  keyPos = sys.argv[3]
##  neighbourhood = "The Oaks"
##  city = "Bakersfield"
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
##  score = 0
  for prop in props:
    propPoly = upland.makePoly(prop['boundaries'])
    if prop['status'] == 'Owned':      
      if len(prop['models']) == 0:
        plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
      elif prop['models'][0]['constructionStatus'] == 'completed':
        if re.search('(?i:(?<!small.)town.house)', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (0, 1, 0))
        elif re.search('(?i:small.town.house(?!.*2))', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 0, 0))
        elif re.search('(?i:small.town.house.*2)', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 0.6, 0))
        elif re.search('(?i:apartment)', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (0, 1, 1))
        elif re.search('(?i:(?<!luxury.)ranch.house)', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (0.717647058823529, 0.717647058823529, 0.717647058823529))
        elif re.search('(?i:lux.*ranch.house)', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 0, 1))
        elif re.search('(?i:lux.*mod.*house)', prop['models'][0]['model']):
          plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (0, 0, 1))
        builtProps += 1
##        score += prop['models'][0]['options']['score']
      elif prop['models'][0]['constructionStatus'] == 'processing' or prop['models'][0]['constructionStatus'] == 'can-watch-ceremony':
        plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 0))
        inProgressProps += 1
##        score += prop['models'][0]['options']['score']
    else:
      plotting.plotObject(canvas, mapFactor, propPoly, minLat, maxLong, (1, 1, 1))
  canvas.set_font_size(100)
  canvas.move_to(75, 75)
  canvas.show_text(f'{neighbourhood}, {city}: {(builtProps/len(props))*100:.0f}% Developed')
  canvas.move_to(75, 165)
  canvas.show_text(f'{builtProps} Completed, {inProgressProps} In Progress')
  today = date.today()
  plotting.plotKey(canvas, surface, 'Dev-key.png', keyPos)
  surface.write_to_png(filename + ' ' + today.strftime('%d-%b') + '.png')

if __name__ == '__main__':
    main()

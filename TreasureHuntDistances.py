import Upland.upland as upland
import Upland.plotting as plotting
import os
import sys
from datetime import date


homedir = os.path.expanduser('~')

headers = {'user-agent': 'nbdBoundaries/1.0'}

city = sys.argv[1]

neighbourhoodPolys = upland.getNeighbourhoodPoly(headers, city)

data = plotting.makeCanvas(neighbourhoodPolys)
surface = data[0]
canvas = data[1]
mapFactor = data[2]
minLat = data[3]
maxLong = data[4]
canvas.set_line_width(4)

for neighbourhoodPoly in neighbourhoodPolys:

  plotting.plotObject(canvas, mapFactor, neighbourhoodPoly, minLat, maxLong)

plotting.plotCircle(canvas, surface, mapFactor, 10000, minLat, maxLong, (0, 0, 0, 0.1))
plotting.plotCircle(canvas, surface, mapFactor, 3000, minLat, maxLong, (0, 0, 0, 0.1))
plotting.plotCircle(canvas, surface, mapFactor, 1000, minLat, maxLong, (0, 0, 0, 0.1))
plotting.plotCircle(canvas, surface, mapFactor, 500, minLat, maxLong, (1, 0, 0, 0.4))
plotting.plotCircle(canvas, surface, mapFactor, 200, minLat, maxLong, (1, 0, 0, 0.6))
plotting.plotCircle(canvas, surface, mapFactor, 50, minLat, maxLong, (1, 0, 0, 0.8))

today = date.today()
canvas.set_source_rgb(0, 0, 0)
canvas.set_font_size(100)
canvas.move_to(75, 75)
canvas.show_text(city)
surface.write_to_png(homedir + '/maps/TreasureHunt/Treasure Hunt Distances ' + city + '.png')

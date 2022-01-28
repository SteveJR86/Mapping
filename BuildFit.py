import Upland.upland as upland
import Upland.plotting as plotting
from shapely import affinity
import math

def checkFit(headers, propID):

  scale = 111139
  
  propDetails = upland.getPropertyDetails(headers, propID)
  propPoly = upland.makePoly(propDetails['boundaries'])
  propPolyNorm = affinity.affine_transform(propPoly, [scale, 0, 0, scale, (-propPoly.bounds[0]*scale), (-propPoly.bounds[1]*scale)])
  hyp1 = math.sqrt(((propPolyNorm.exterior.coords[1][0]-propPolyNorm.exterior.coords[0][0])**2)+((propPolyNorm.exterior.coords[1][1]-propPolyNorm.exterior.coords[0][1])**2))
  hyp2 = math.sqrt(((propPolyNorm.exterior.coords[2][0]-propPolyNorm.exterior.coords[1][0])**2)+((propPolyNorm.exterior.coords[2][1]-propPolyNorm.exterior.coords[1][1])**2))
  if hyp1 > hyp2:
    opp = propPolyNorm.exterior.coords[1][1] - propPolyNorm.exterior.coords[0][1]
    adj = propPolyNorm.exterior.coords[0][0] - propPolyNorm.exterior.coords[1][0]
  else:
    opp = propPolyNorm.exterior.coords[2][1] - propPolyNorm.exterior.coords[1][1]
    adj = propPolyNorm.exterior.coords[1][0] - propPolyNorm.exterior.coords[2][0]
  angle = math.degrees(math.atan(opp/adj))
  propPolyRot = affinity.rotate(propPolyNorm, 90+angle)

  buildPossible = {}
  buildTypes = upland.getBuildings(headers, propID)
  for buildType in buildTypes:
    buildPoly = upland.makePoly({'type': 'Polygon', 'coordinates': [buildType['boundaries']]})
    buildPolyNorm = affinity.affine_transform(buildPoly, [3, 0, 0, 3, (-buildPoly.bounds[0]*3), (-buildPoly.bounds[1]*3)])
    
    buildPolyCentered = affinity.affine_transform(buildPolyNorm, [1, 0, 0, 1, -(buildPolyNorm.centroid.coords[0][0] - propPolyRot.centroid.coords[0][0]), -(buildPolyNorm.centroid.coords[0][1] - propPolyRot.centroid.coords[0][1])])
    if buildPolyCentered.within(propPolyRot):
      buildPossible[buildType['buildingImage']] = True
    else:
      buildPossible[buildType['buildingImage']] = False

  return buildPossible

def main():
  headers = {'user-agent': 'buildfit/1.0'}
  propID = 81450433868377

  response = checkFit(headers, propID)
  for x, y in response.items():
    if y:
      print(f'Building type {x.split("/")[0].replace("_", " ").replace(" new", "").replace("2", " 2")} will fit')
    else:
      print(f'Building type {x.split("/")[0].replace("_", " ").replace(" new", "").replace("2", " 2")} will not fit')
  
  return

if __name__ == '__main__':
  main()

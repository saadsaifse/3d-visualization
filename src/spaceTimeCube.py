import sys, os, ogr
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

currentFilePath = sys.argv[0]
currentFileDir = os.path.dirname(currentFilePath)
gpxPath = os.path.join(currentFileDir, '..', 'data', 'muenster.gpx')

absGpxPath = os.path.abspath(gpxPath)

print("GPX path is: ", gpxPath)
print("Abs GPX path is: ", absGpxPath)

gpxDriver = ogr.GetDriverByName("GPX")
gpx = gpxDriver.Open(absGpxPath, 0)
layer = gpx.GetLayer(4) #get track points of gpx only

layerDef = layer.GetLayerDefn()

timeFieldExists = False
for i in range(layerDef.GetFieldCount()):
    if layerDef.GetFieldDefn(i).name == 'time':
        timeFieldExists = True
        break

if timeFieldExists == False:
    print("time field does not exist in the GPX file. Terminating..")
    sys.exit(1)

lat = [] 
lon = []
minutes = []

startTime = None
endTime = None
for feat in layer:
    geom = feat.geometry()
    lat.append(geom.GetX())
    lon.append(geom.GetY())
    time = feat.GetField('time')
    endTime = datetime.strptime(time, "%Y/%m/%d %H:%M:%S+00")
    if (startTime == None):
        startTime = endTime
    timeDiff = endTime - startTime
    minutes.append(timeDiff.seconds/60)

fig = plt.figure()
ax = fig.gca(projection='3d')
plt.suptitle('Space Time Cube', fontsize=14, fontweight='bold')
plt.title('From {} to {}'.format(startTime, endTime))

ax.plot(lat, lon, minutes)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Minutes')

plt.show()
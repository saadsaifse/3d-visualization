import sys, os, gdal
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

currentFilePath = sys.argv[0]
currentFileDir = os.path.dirname(currentFilePath)
#demPath = os.path.join(currentFileDir, '..', 'data', 'Muenster.tif')
demPath = os.path.join(currentFileDir, '..', 'data', 'DEM_NRW_100Meter.tif')

absDemPath = os.path.abspath(demPath)

print("DEM path is: ", demPath)
print("Abs DEM path is: ", absDemPath)

dem = gdal.Open(absDemPath)
gt = dem.GetGeoTransform()

demArray = dem.ReadAsArray()

demArrayRows = demArray.shape[0]
demArrayColumns = demArray.shape[1]

# add threshold of 10 for z-axis
verticalMin = demArray.min() + 10 if demArray.min() >= 0 else demArray.min() - 10
verticalMax = demArray.max() + 10 if demArray.max() >= 0 else demArray.max() - 10

pixelWidth = gt[1]
pixelHeight = gt[5]

rasterOriginX = gt[0]
rasterOriginY = gt[3]

X = np.arange(rasterOriginX, rasterOriginX + demArrayColumns * pixelWidth, pixelWidth)
Y = np.arange(rasterOriginY, rasterOriginY + demArrayRows * pixelHeight, pixelHeight)

X, Y = np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surface = ax.plot_surface(X, Y, demArray, rstride=1, cstride=1, cmap=plt.get_cmap('terrain'), vmin=verticalMin, vmax=verticalMax, linewidth=0, antialiased=False)

ax.set_xlabel(r'$X$')
ax.set_ylabel(r'$Y$')
ax.set_zlabel(r'$Elevation$')

fig.colorbar(surface, shrink=0.5, aspect=20)

plt.show()
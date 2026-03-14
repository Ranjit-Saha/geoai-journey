# ================================================================
#  create_sample_data.py [Day 1]
# ================================================================
#    1) Create synthetic satellite data for learning
#    2) This mimics Sentinel-2 structure but is small and simple
# ================================================================
# ================================================================
import numpy as np
import rasterio
from rasterio.transform import from_bounds

# Image size (small for practice)
height, width = 100, 100

# =================================================================
# Create 4 bands (Blue, Green, Red, NIR)
# Simulate different land covers:
# Top-left: Vegetation (high NIR, low Red)
# Top-right: Water (low everything)
# Bottom-left: bare soil (medium everything)
# Bottom-right: Urban (high everything)
# =================================================================

# Initialize
blue = np.zeros((height, width), dtype=np.uint16)
green = np.zeros((height, width), dtype=np.uint16)
red = np.zeros((height, width), dtype=np.uint16)
nir = np.zeros((height, width), dtype=np.uint16)

# print(blue)

# Fill quadrants: Vegetation (top-left)
blue[0:50, 0:50] = 400
green[0:50, 0:50] = 600
red[0:50, 0:50] = 300
nir[0:50, 0:50] = 3000  # High NIR!

# Fill quadrants: Water (top-right)
blue[0:50, 50:100] = 800
green[0:50, 50:100] = 600
red[0:50, 50:100] = 300
nir[0:50, 50:100] = 100  # Low NIR!

# Fill quadrants: Bare soil (Bottom-left)
blue[50:100, 0:50] = 1200
green[50:100, 0:50] = 1400
red[50:100, 0:50] = 1500
nir[50:100, 0:50] = 1800

# Fill quadrants: Urban (Bottom-right)
blue[50:100, 50:100] = 1800
green[50:100, 50:100] = 1900
red[50:100, 50:100] = 2000
nir[50:100, 50:100] = 2100

# ======================================================
# Under the hood:
# ======================================================
# blue[0:50, 0:50] = 400 # top-left
# blue[0:50, 50:100] = 800 # top-right
# blue[50:100, 0:50] = 1200 # bottom-left
# blue[50:100, 50:100] = 1800 # bottom-right
#
# =======================================
# Output:-
# =======================================
# print('Blue Band:\n', blue)
# print('Green Band:\n', green)
# print('Red Band:\n', red)
# print('NIR Band:\n', nir)
#
#  Blue Band:
#  [[ 400  400  400 ...  800  800  800]
#  [ 400  400  400 ...  800  800  800]
#  [ 400  400  400 ...  800  800  800]
#  ...
#  [1200 1200 1200 ... 1800 1800 1800]
#  [1200 1200 1200 ... 1800 1800 1800]
#  [1200 1200 1200 ... 1800 1800 1800]]
# Green Band:
#  [[ 600  600  600 ...  600  600  600]
#  [ 600  600  600 ...  600  600  600]
#  [ 600  600  600 ...  600  600  600]
#  ...
#  [1400 1400 1400 ... 1900 1900 1900]
#  [1400 1400 1400 ... 1900 1900 1900]
#  [1400 1400 1400 ... 1900 1900 1900]]
# Red Band:
#  [[ 300  300  300 ...  300  300  300]
#  [ 300  300  300 ...  300  300  300]
#  [ 300  300  300 ...  300  300  300]
#  ...
#  [1500 1500 1500 ... 2000 2000 2000]
#  [1500 1500 1500 ... 2000 2000 2000]
#  [1500 1500 1500 ... 2000 2000 2000]]
# NIR Band:
#  [[3000 3000 3000 ...  100  100  100]
#  [3000 3000 3000 ...  100  100  100]
#  [3000 3000 3000 ...  100  100  100]
#  ...
#  [1800 1800 1800 ... 2100 2100 2100]
#  [1800 1800 1800 ... 2100 2100 2100]
#  [1800 1800 1800 ... 2100 2100 2100]]
#
# ======================================================

# Add some noise (realistic)
blue = blue + np.random.randint(0, 50, (height, width))
green = green + np.random.randint(0, 50, (height, width))
red = red + np.random.randint(0, 50, (height, width))
nir = nir + np.random.randint(0, 50, (height, width))

# Stack bands
image_data = np.stack([blue, green, red, nir])

# Geographic information for Dhaldabri, West Bengal
# Roughly centered around:
# west = 89.69
# south = 26.30
# east = 89.79
# north = 26.40

transform = from_bounds(
    west=89.69,
    south=26.30,
    east=89.79,
    north=26.40,
    width=width,
    height=height
)

# Save as GeoTIFF
with rasterio.open(
    'data/sample_sentinel2.tif', 'w',
    driver= 'GTiff',
    height=height,
    width=width,
    count=4, # 4-bands
    dtype=image_data.dtype,
    crs='EPSG:4326', # WGS84 Coordinate System
    transform=transform,
)as dst:
    dst.write(image_data)

    # Add band descriptions
    dst.set_band_description(1, 'Blue')
    dst.set_band_description(2, 'Green')
    dst.set_band_description(3, 'Red')
    dst.set_band_description(4, 'NIR')

print("✅ Created sample_sentinel2.tiff")
print(f"Size: {height}x{width} Pixels")
print(f"Bands: 4 (Blue, Green, Red, NIR)")
print(f"Location: Dhaldabri, West Bengal (approximately)")

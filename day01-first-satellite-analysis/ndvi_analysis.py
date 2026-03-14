# ================================================================
#  ndvi_analysis.py
# ================================================================
#    Day 1: First Satellite Data Analysis :)
#    Calculate NDVI from Sentinel-2 data
# Author: Ranjit Saha
# Date: 12 March, 2026
# ================================================================
# ================================================================

# Step 1: Import Libraries
import numpy as np
import rasterio
import matplotlib.pyplot as plt

print("=" * 50)
print("DAY 1 : NDVI CALCULATION")
print("=" * 50)

# Step 2: Load the Satellite image
print("\n1. Loading Satellite image...")

# Open the GeoTIFF file
with rasterio.open('data/sample_sentinel2.tif') as src:
    # Print basic information
    print(f" Image Size: {src.width}x{src.height} Pixels")
    print(f" Number of bands: {src.count}")
    print(f" Coordinate System: {src.crs}")
    print(f" Geographic bounds: {src.bounds}")

    # Read bands
    # Band 1 = Blue Band 2 = Green Band 3 = Red Band 4 = NIR
    blue = src.read(1) # Read 1st band
    green = src.read(2) # Read 2nd band
    red = src.read(3) # Read 3rd band
    nir = src.read(4) # Read 4th band

    # Save transform for later
    transform = src.transform
    crs = src.crs

    print("✅Image loaded successfully!")

# Step 3: Explore the data (red, nir)
print("\n2. Exploring band values...")
print(f" Red band --> Min: {red.min()}, Max: {red.max()}, Mean: {red.mean():.1f}")
print(f" NIR band --> Min: {nir.min()}, Max: {nir.max()}, Mean: {nir.mean():.1f}")

# Step 4: Calculate NDVI
print("\n3. Calculating NDVI...")

# Convert to float (required for division)
red = red.astype(float)
nir = nir.astype(float)

# NDVI formula: (NIR - Red) / (NIR + Red)
# Add small number to denominator to avoid division by zero
denominator = nir + red
denominator = np.where(denominator==0, 0.0001, denominator)

ndvi = (nir - red) / denominator

print(f" NDVI --> Min: {ndvi.min():.3f}, Max: {ndvi.max():.3f}, Mean: {ndvi.mean():.3f}")

# Step 5: Interpret results
print("\n5. Interpreting NDVI values...")

# Count Pixels in each category
water_mask = ndvi < 0
bare_soil_mask = (ndvi >= 0) & (ndvi < 0.3)
vegetation_mask = (ndvi > 0.3) & (ndvi < 0.6)
dense_veg_mask =  ndvi >= 0.6

total_pixels = ndvi.size

print(f" Water/Snow: {water_mask.sum()} Pixels ({water_mask.sum() / total_pixels * 100:.1f}%)")
print(f" Bare soil/Stressed: {bare_soil_mask.sum()} Pixels ({bare_soil_mask.sum() / total_pixels * 100:.1f}%)")
print(f" Moderate vegetation: {vegetation_mask.sum()} Pixels ({vegetation_mask.sum() / total_pixels * 100:.1f}%)")
print(f" Dense vegetation: {dense_veg_mask.sum()} Pixels ({dense_veg_mask.sum() / total_pixels * 100:.1f}%)")

# Step 6: Create visualization
print("\n6. Creating visualization...")

fig, axes = plt.subplots(2,3, figsize=(15, 10))
fig.suptitle('Day 1: My First Satellite Data Analysis', fontsize=16, fontweight='bold')

# Plot 1: Red Band
axes[0, 0].imshow(red, cmap='Reds')
axes[0, 0].set_title('Red Band')
axes[0, 0].axis('off')

# Plot 2: NIR Band
axes[0, 1].imshow(nir, cmap='YlGn')
axes[0, 1].set_title('NIR Band')
axes[0, 1].axis('off')

# Plot 3: RGB composite (true color)
# Normalize for display
rgb = np.dstack([
    (red - red.min()) / (red.max() - red.min()),
    (green - green.min()) / (green.max() - green.min()),
    (blue - blue.min()) / (blue.max() - blue.min())

])
axes[0, 2].imshow(rgb)
axes[0, 2].set_title('True color (RGB)')
axes[0, 2].axis('off')

# Plot 4: NDVI Map
im = axes[1, 0].imshow(ndvi, cmap='RdYlGn', vmin= -1, vmax= 1)
axes[1, 0].set_title('NDVI (Vegetation Index)')
axes[1, 0].axis('off')

plt.colorbar(im, ax=axes[1, 0], fraction=0.046)

# Plot 5: NDVI histogram
axes[1, 1].hist(ndvi.ravel(), bins=50, color='green', edgecolor='black')
axes[1, 1].set_xlabel('NDVI Value')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('NDVI Distribution')
axes[1, 1].axvline(0.3, color='red', linestyle='--', label='Vegetation threshold')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Plot 6: Vegetation classification
classified = np.zeros_like(ndvi)
classified[water_mask] = 0
classified[bare_soil_mask] = 1
classified[vegetation_mask] = 2
classified[dense_veg_mask] = 3

im2 = axes[1, 2].imshow(classified, cmap='terrain')
axes[1, 2].set_title('Land cover classification')
axes[1, 2].axis('off')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='blue', label='Water'),
    Patch(facecolor='brown', label='Bare soil'),
    Patch(facecolor='lightgreen', label='Moderate vegetation'),
    Patch(facecolor='darkgreen', label='Dense vegetation')

]

axes[1, 2].legend(handles=legend_elements, loc='upper right')
plt.tight_layout()
plt.savefig('outputs/day1_ndvi_analysis.png', dpi=300, bbox_inches='tight')

print("✅Saved visualization: outputs/day1_ndvi_analysis.png")

# plt.show()

# Step 7: Save NDVI as GeoTIFF
print("\n6. Saving NDVI as GeoTIFF...")

with rasterio.open( 'outputs/ndvi_result.tif', 'w',
        driver='GTiff',
        height=ndvi.shape[0],
        width=ndvi.shape[1],
        count=1,
        dtype=ndvi.dtype,
        crs=crs,
        transform=transform,
) as dst:
    dst.write(ndvi, 1)
    dst.set_band_description(1, 'NDVI')

print("✅Saved NDVI GeoTIFF: outputs/ndvi_result.tif")


# Step 8: Summary Statistics
print("\n" + "=" * 50)
print("ANALYSIS COMPLETE!")
print("=" * 50)

print(f" Processed {total_pixels:,} Pixels")
print(f" Average NDVI: {ndvi.mean():.3f}")
print(f" Healthy vegetation coverage: {vegetation_mask.sum() + dense_veg_mask.sum() / total_pixels * 100:.1f}%")
print("\nYou just analyzed satellite data from space!")
print("=" * 50)





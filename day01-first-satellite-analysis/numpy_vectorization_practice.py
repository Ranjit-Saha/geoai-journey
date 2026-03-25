# ==================================================================================
#  numpy_vectorization_practice.py
# ==================================================================================
#    Day1 completion: Numpy Vectorization
#    Why this matters:
#    Processing a 10,000 x 10,000 satellite image pixel by pixel
#    takes hours. Vectorization takes seconds.
# Author: Ranjit Saha
# Date: 25 March, 2026
# ==================================================================================
# ==================================================================================
import numpy as np
import time

print("=" * 50)
print("NUMPY VECTORIZATION - WHY IT MATTERS FOR SATELLITE DATA")
print("=" * 50)

# Simulate a small satellite image (1000x1000 pixels)
height, widtth = 1000, 1000
red_band = np.random.randint(100, 500, (height, widtth), dtype=np.uint16)
nir_band = np.random.randint(500, 3000, (height, widtth), dtype=np.uint16)

print(f"\nImage size: {height}X{widtth} = {height * widtth:,} pixels")

# ====================================================================================
# Method 1: Loop (the wrong way)
# ====================================================================================
print("\n1. Loop method (SLOW)...")
start = time.time()
ndvi_loop = np.zeros((height, widtth))
for i in range(height):
    for j in range(widtth):
        r = float(red_band[i, j])
        n = float(nir_band[i, j])
        if (n + r) > 0:
            ndvi_loop[i, j] = (n - r) / (n + r)
loop_time = time.time() - start
print(f" Time: {loop_time:.2f} seconds")

# ====================================================================================
# Method 2: Vectorized (the right way)
# ====================================================================================
print("\n2. Vectorized method (FAST)...")
start = time.time()
red_f = red_band.astype(np.float32)
nir_f = nir_band.astype(np.float32)

denominator = nir_f + red_f
denominator = np.where(denominator == 0, 0.0001, denominator)
ndvi_vectorized = (nir_f - red_f) / denominator

vector_time = time.time() - start
print(f" Time: {vector_time:.4f} seconds")

speedup = loop_time / vector_time
print(f"\n SPEEDUP: {speedup:.0f} X FASTER")
print(f" For a real Sentinel-2 scene (10980x10980 pixels): ")
print(f" Loop would take: {loop_time * 120:.0f} seconds")
print(f" Vectorized takes: {vector_time * 120:.1f} seconds")

# ===================================================================================
# KEY INSIGHT
# ===================================================================================
print("\n" + "=" * 50)
print("KEY INSIGHT FOR INTERVIEWS:")
print("=" * 50)
print("""
Numpy vectorization works because operations are applied to the entire array at once using optimized C code under the hood.
A Sentinel-2 scene has ~120 million pixels.
- Processing them one by one in python is not engineering.
- Processing them as arrays is.""")

# Day 1 - March 12, 2026 

##📁 File Structure  
``` 
day01-first-satellite-analysis/
├── data/                    ← sample_sentinel2.tif
├── outputs/                 ← ndvi_result.tif, day1_ndvi_analysis.png
├── notebooks/
├── create_sample_data.py
├── ndvi_analysis.py
├── numpy_vectorization_practice.py
├── README.md
└── requirements.txt
```
## 🧑‍💻 Completed
- Satellite data theory: bands, GeoTIFF, spectral signatures (e.g., how a leaf reflects light from blue, green, red, to infrared)
- Built NDVI calculator from scratch (ndvi_analysis.py)
- Created synthetic Sentinel-2 data and ran analysis (create_sample_data.py)
- Understood: satellite image = grid of numbers, not a photo
- Numpy Vectorization
## 📚Key Insight
📗Healthy plants are Bright in NIR (due to High Reflectance), Dark in Red (due to High Absorption).
This invisible difference is how we monitor crops from space.

📙Numpy vectorization Why this matters: Processing a 10,000 x 10,000 satellite image pixel by pixel takes hours. Vectorization takes seconds.

Numpy vectorization works because operations are applied to the entire array at once using optimized C code under the hood.

A Sentinel-2 scene has ~120 million pixels:
- Processing them one by one in python is not engineering.
- Processing them as arrays is.
## 🔳Outputs
> ✅Saved visualization: outputs/day1_ndvi_analysis.png
 ![NDVI ANALYSIS](outputs/day1_ndvi_analysis.png)

> ✅Saved NDVI as GeoTIFF: outputs/ndvi_result.tif

> ✅Numpy Vectorization: 

Image size: 1000X1000 = 1,000,000 pixels
1. Loop method (SLOW)...
Time: 0.95 seconds

2. Vectorized method (FAST)...
 Time: 0.0156 seconds

 🚅SPEEDUP: 61 X FASTER <br>
 For a real Sentinel-2 scene (10980x10980 pixels): 
 - Loop would take: 115 seconds
 - Vectorized takes: 1.9 seconds

## ⛷️Skipped
- Streamlit deployment (scheduled for Day 6)
- LinkedIn post (will do shortly)

## 😎Confidence
- Satellite concepts: 8/10
- NDVI code: 8/10
- Git workflow: 6/10

## 🪦Tomorrow: Coordinate Reference Systems (CRS) 
- WGS84 vs UTM
- EPSG codes
- Projection converter tool
- PostGIS installation



# 🌍 GeoAI Journey: Day 1 — Satellite Analysis & NumPy Vectorization

Welcome to Day1 of GeoAI intensive. Today's focus was shifting from "images as photos" to **"images as geospatial data,"** specifically calculating the **Normalized Difference Vegetation Index (NDVI)** using highly optimized Python workflows.

## 🚀 Quick Start
To replicate this analysis locally:

1. **Clone the repository:**
```bash
    git clone https://github.com/Ranjit-Saha/geoai-journey.git
``` 
2. **Navigate to Day 1:**
``` 
cd geoai-journey/day01-first-satellite-analysis
```
3. **Install dependencies::**
``` 
pip install -r requirements.txt

```
4. **Run the analysis::**
```commandline
python ndvi_analysis.py

```


## 📁 File Structure  
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

## 🧑‍💻 Technical Achievements

- *Satellite Theory:* Mastered spectral signatures. Healthy vegetation reflects Near-Infrared (NIR) and absorbs Red light.
- **NDVI from Scratch:** Implemented the formula: NDVI = (NIR - Red) / (NIR + Red).
- *Synthetic Data Generation:* Built a generator to create multi-band GeoTIFFs to simulate Sentinel-2 data.
- *Optimization:* Proved that Python for-loops are a bottleneck for Geospatial Big Data.

## 📚 Key Insights
📗 The Science of NDVI

Healthy plants appear Bright in NIR (High Reflectance) and Dark in Red (High Absorption). This mathematical difference allows us to monitor crop health and deforestation globally.

📙 Why Vectorization?

A standard Sentinel-2 scene contains ~120 million pixels. Processing these one-by-one is inefficient. By using NumPy Vectorization, we perform calculations on the entire array simultaneously using optimized C code.


## 🔳 Performance Benchmark
Benchmarked on a 1,000 x 1,000 pixel test image:

| Method | Execution Time | Efficiency |
|--------|----------------|-------------|
|Standard Loop|	0.95 seconds|	1x (Baseline)|
|NumPy Vectorized|	0.015 seconds|	**61x Faster 🚅**|

> **Scalability:** For a full Sentinel-2 scene (10,980px), a loop takes **~2 minutes**. Vectorization takes **~2 seconds**.

---
## 🖼️ Results & Visualization
> ###### ✅Saved visualization: outputs/day1_ndvi_analysis.png
 ![NDVI ANALYSIS](outputs/day1_ndvi_analysis.png)

NDVI Analysis Map

Visualizing plant health: Green represents high biomass/healthy vegetation, while red/yellow indicates soil or stressed areas.
> ###### ✅Saved NDVI as GeoTIFF: outputs/ndvi_result.tif

  

> ##### ✅Numpy Vectorization: 

Image size: 1000X1000 = 1,000,000 pixels
1. Loop method (SLOW)...
Time: 0.95 seconds
 2. Vectorized method (FAST)...
 Time: 0.0156 seconds

 🚅SPEEDUP: 61 X FASTER <br>
 For a real Sentinel-2 scene (10980x10980 pixels): 
 - Loop would take: 115 seconds
 - Vectorized takes: 1.9 seconds

 ---
## ⛷️ Status & Progress
- NDVI Calculator Implementation
- NumPy Vectorization Speed Benchmarking
- Streamlit Dashboard Integration (Planned for Day 6)
 
## 😎Confidence Score:
- Satellite Concepts: 🟢 8/10
- NDVI Code: 🟢 8/10
- Git Workflow: 🟡 6/10

## 🪦Tomorrow: Coordinate Reference Systems (CRS) 
- **WGS84 vs UTM:** Why projections matter.
- **EPSG Codes:** The "ZIP codes" of maps.
- Projection converter tool
- **PostGIS:** Installing the world's most powerful spatial database.



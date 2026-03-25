# 🛰️ Agri-Sentry 360: The 90-Day GeoAI Journey
**Project by Ranjit Saha | Planetary Physician**

> "The Earth is my Patient. Satellites are my X-Ray. GenAI is my Diagnosis."

This repository documents the 90-session build of **Agri-Sentry 360**—a climate-resilient agricultural intelligence platform for the farmers of **Dhaldabri, West Bengal**. We are solving the $6B Trust Gap using Sentinel-1 SAR, PyTorch U-Net, and Agentic AI.

---

## 📈 90-Session Master Log

| Session | Module | Key Deliverable | Interview Skill | Status |
|:---:|:---|:---|:---|:---:|
| **01** | [Foundations](./day01-first-satellite-analysis/) | Built NDVI calculator; 61x NumPy speedup | Spectral Signatures | ✅ |
| **02** | [CRS & PostGIS](./day02-crs-postgis/) | Coordinate systems & PostGIS setup | WGS84 vs UTM | 🏗️ |
| **03** | Spatial Ops | GeoPandas joins & farm boundaries | Spatial Indexing | 📅 |
| **04** | Rasterio | Multi-band Sentinel-2 processing | GeoTIFF Metadata | 📅 |
| **05** | ETL Pipeline | SoilGrids + Open-Meteo Integration | Data Engineering | 📅 |

---

## 📂 Repository Structure
*   `agri-sentry360/`: The Hero Project (src, docs, deployment).
*   `day01-first-satellite-analysis/`: Technical foundation files.
*   `notebooks/`: Research and prototyping rabbit holes.
*   `requirements.txt`: Global dependencies.

---

## 🚀 The Mission: Dhaldabri to the World
During monsoon, optical satellites go blind. Farmers in the Terai lose crops to floods with zero warning. My mission is to build a **System of Truth**:
1.  **SAR Flood Detection**: Seeing through clouds when others are blind.
2.  **Sowing Window Engine**: 5-year historical flood analysis for optimal planting.
3.  **Bengali Voice Chatbot**: The "Stethoscope" connecting AI to the farmer.

---

## 🛠️ Tech Stack
*   **EO:** Sentinel-1 (SAR), Sentinel-2, Google Earth Engine.
*   **AI:** PyTorch, TorchGeo, LangGraph, RAG.
*   **Spatial:** PostGIS, GDAL, GeoPandas, Rasterio.
*   **Cloud:** FastAPI, Docker, AWS (EC2, RDS, S3).

---

## 📬 Connectivity
[LinkedIn](https://www.linkedin.com) 

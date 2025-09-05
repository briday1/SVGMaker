# Raster ➜ SVG Converter (Streamlit)

A simple web UI to convert raster images (PNG/JPG/WebP/BMP) into SVG with live preview.

## Features
- **Regions (fills)**: Posterize to N colors and trace filled shapes (Pillow quantize + contour tracing).
- **Edges (strokes)**: Canny edge detect and trace polylines as stroked paths.
- Adjustable **simplification**, **min area/length**, **pre-blur**, **stroke width**, background, and output **scale**.
- Side-by-side original/preview and an **SVG preview** with download.

## Install & Run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
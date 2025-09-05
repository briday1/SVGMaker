# app.py — Line Drawing to SVG Converter using ImageMagick and Potrace
from __future__ import annotations
import base64
import subprocess
from typing import Tuple

import streamlit as st
from PIL import Image

def encode_svg_data_uri(svg_str: str) -> str:
    b64 = base64.b64encode(svg_str.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"

def run_system_calls(input_path: str, threshold: int, turdsize: int, alphamax: float, line_width: float) -> str:
    """Run ImageMagick's convert and Potrace to generate SVG."""
    # Convert image to PBM using ImageMagick
    pbm_path = f"{input_path}.pbm"
    subprocess.run([
        "convert", input_path, "-threshold", f"{threshold}%%", pbm_path
    ], check=True)

    # Run Potrace to convert PBM to SVG
    svg_path = f"{input_path}.svg"
    subprocess.run([
        "potrace", pbm_path, "--svg", "--turdsize", str(turdsize), "--alphamax", str(alphamax), "-o", svg_path
    ], check=True)

    # Read the generated SVG
    with open(svg_path, "r") as svg_file:
        svg_content = svg_file.read()

    # Ensure black lines with adjustable thickness
    svg_content = svg_content.replace(
        '<path ',
        f'<path stroke="#000000" stroke-width="{line_width}" '
    )

    return svg_content

st.set_page_config(page_title="Line Drawing ➜ SVG Converter", layout="wide")
st.title("✏️ Line Drawing ➜ SVG Converter")
st.caption("Convert line drawings to SVG using ImageMagick and Potrace.")

with st.sidebar:
    st.header("Settings")
    threshold = st.slider("Threshold (%)", 0, 100, 50, 1)
    turdsize = st.slider("Turdsize (min path size)", 0, 100, 2, 1)
    alphamax = st.slider("Alphamax (curve optimization)", 0.0, 1.0, 1.0, step=0.1)
    line_width = st.slider("Line Width", 0.1, 20.0, 1.0, step=0.1)

uploaded = st.file_uploader("Upload a line drawing (PNG/JPG)", type=["png", "jpg", "jpeg"])
col1, col2 = st.columns(2, gap="large")

if uploaded is None:
    with col1:
        st.info("Upload an image to begin.")
else:
    # Save the uploaded image to a temporary file
    input_path = "uploaded_image.png"
    with open(input_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Run the system calls to generate SVG
    try:
        svg_markup = run_system_calls(input_path, threshold, turdsize, alphamax, line_width)

        with col1:
            st.subheader("Original")
            st.image(uploaded, use_container_width=True)

        with col2:
            st.subheader("SVG Preview")
            # Add a white background for the preview only
            preview_markup = svg_markup.replace(
                '<svg ',
                '<svg style="background-color:#FFFFFF;" '
            )
            data_uri = encode_svg_data_uri(preview_markup)
            st.markdown(f'<img src="{data_uri}" style="max-width:100%; height:auto;" />', unsafe_allow_html=True)
            st.download_button("Download SVG", data=svg_markup.encode("utf-8"), file_name="output.svg", mime="image/svg+xml")

    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred while processing the image: {e}")
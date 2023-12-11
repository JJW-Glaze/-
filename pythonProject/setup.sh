mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
echo "packages:
- freeglut3-dev
- libgtk2.0-dev
- libgl1-mesa-glx
- tesseract-ocr
- libtesseract-dev
- libtesseract4
- tesseract-ocr-all
" > ~/.streamlit/packages.txt

#!/bin/bash

echo "[TERMINAL] Define virtual environment path inside /output"
VENV_DIR="output/venv"

echo "[TERMINAL] Check if /output exists, if not, create it"
if [ ! -d "output" ]; then
    mkdir -p output
fi

echo "[TERMINAL] Check if virtual environment exists, if not, create it"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
    echo "[TERMINAL] Virtual environment created at $VENV_DIR"
fi

echo "[TERMINAL] Activate the virtual environment"
source $VENV_DIR/bin/activate

echo "[TERMINAL] Upgrade pip to avoid warnings"
pip install --upgrade pip

echo "[TERMINAL] Install dependencies"
pip install -r resources/requirements.txt

echo "[TERMINAL] Check if the data.csv exists in the output folder, if not, generate it"
if [ ! -f "output/data.csv" ]; then
    echo "[TERMINAL] output/data.csv not found. Generating sample data..."
    python3 resources/generate_data.py
else
    echo "[TERMINAL] output/data.csv already exists. Skipping data generation."
fi

echo "[TERMINAL] Check if the processed Parquet file already exists"
if [ ! -f "output/data.parquet" ]; then
    echo "[TERMINAL] Run the Python script to read CSV and convert it to Parquet"
    python3 resources/read_data.py \
        --input output/data.csv \
        --output output/data.parquet \
        --chunk_size 500000
else
    echo "[TERMINAL] output/data.parquet already exists. Skipping conversion to Parquet."
fi

echo "[TERMINAL] Run the visualization script"
python3 resources/visualize_data.py \
    --input_parquet output/data.parquet \
    --output_dir output

echo "[TERMINAL] Deactivate the virtual environment"
deactivate

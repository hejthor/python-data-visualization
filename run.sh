#!/bin/bash

# Define virtual environment path inside /output
VENV_DIR="output/venv"

# Check if /output exists, if not, create it
if [ ! -d "output" ]; then
    mkdir -p output
fi

# Check if virtual environment exists, if not, create it
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
    echo "Virtual environment created at $VENV_DIR"
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip to avoid warnings
pip install --upgrade pip

# Install dependencies
pip install -r resources/requirements.txt

# Check if the data.csv exists in the output folder, if not, generate it
if [ ! -f "output/data.csv" ]; then
    echo "output/data.csv not found. Generating sample data..."
    python3 resources/generate_data.py
else
    echo "output/data.csv already exists. Skipping data generation."
fi

# Check if the HDF5 file already exists
if [ ! -f "output/data.h5" ]; then
    # Run the Python script to process large CSV to HDF5
    python3 resources/read_data.py \
        --input output/data.csv \
        --output output/data.h5 \
        --chunk_size 50000
else
    echo "output/data.h5 already exists. Skipping CSV processing."
fi

# Run the visualization script
python3 resources/visualize_data.py \
    --hdf5_file output/data.h5 \
    --output_image output/graph.png

# Deactivate the virtual environment
deactivate

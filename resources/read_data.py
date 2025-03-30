import pandas as pd
import argparse

def process_chunk(chunk):
    """Process each chunk if needed (e.g., filtering, transformations)."""
    chunk.columns = [col.lower() for col in chunk.columns]  # Example transformation
    return chunk

def read_large_csv_hdf5(input_csv, output_hdf5, chunk_size):
    """Read large CSV in chunks and save as an optimized HDF5 file."""
    store = pd.HDFStore(output_hdf5, mode='w', complevel=9, complib='blosc')  # High compression

    for i, chunk in enumerate(pd.read_csv(input_csv, chunksize=chunk_size, delimiter=';')):
        chunk = process_chunk(chunk)

        # Append to HDF5 file
        store.append('data', chunk, format='table', data_columns=True)

    store.close()
    print(f"File saved as {output_hdf5}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process large CSV to HDF5 format.")
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--output", type=str, required=True, help="Path to output HDF5 file")
    parser.add_argument("--chunk_size", type=int, default=100000, help="Chunk size for processing")
    
    args = parser.parse_args()
    read_large_csv_hdf5(args.input, args.output, args.chunk_size)

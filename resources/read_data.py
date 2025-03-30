import pandas as pd
import argparse

def process_chunk(chunk):
    """Process each chunk if needed (e.g., filtering, transformations)."""
    chunk.columns = [col.lower() for col in chunk.columns]  # Example transformation
    return chunk

def read_large_csv_parquet(input_csv, output_parquet, chunk_size):
    """Read large CSV in chunks and save as a processed Parquet file."""
    processed_data = []

    # Read and process the CSV file in chunks
    for chunk in pd.read_csv(input_csv, chunksize=chunk_size):
        chunk = process_chunk(chunk)
        processed_data.append(chunk)

    # Combine all chunks into a single DataFrame
    final_df = pd.concat(processed_data, ignore_index=True)
    
    # Save the processed DataFrame to Parquet
    final_df.to_parquet(output_parquet, compression='snappy')  # Save with Snappy compression
    print(f"File saved as {output_parquet}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process large CSV to Parquet format.")
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--output", type=str, required=True, help="Path to output Parquet file")
    parser.add_argument("--chunk_size", type=int, default=500000, help="Chunk size for processing")
    
    args = parser.parse_args()
    read_large_csv_parquet(args.input, args.output, args.chunk_size)

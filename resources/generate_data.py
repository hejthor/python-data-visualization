import pandas as pd
import numpy as np
import os

def generate_sample_data(output_path):
    """Generate a sample dataset and save it to a CSV file."""
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Sample column names
    columns = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10']
    
    # Generate random data for each column
    data = np.random.rand(10000000, len(columns))  # rows of random numbers
    df = pd.DataFrame(data, columns=columns)
    
    # Save the dataframe to CSV in the output folder
    output_file = os.path.join(output_path, 'data.csv')
    df.to_csv(output_file, index=False, sep=';')  # Save with semicolon separator
    print(f"Generated sample data and saved to {output_file}")

if __name__ == "__main__":
    output_path = 'output'  # Set output folder
    generate_sample_data(output_path)
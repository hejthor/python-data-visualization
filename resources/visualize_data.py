import pandas as pd
import matplotlib.pyplot as plt
import argparse

def visualize_data(hdf5_file, output_image):
    """Read data from HDF5 and generate a plot."""
    # Read data from HDF5 file
    data = pd.read_hdf(hdf5_file, key='data')

    # Strip whitespace from column names (in case there are any)
    data.columns = data.columns.str.strip()

    # Print the column names (headers) for debugging purposes
    print("Headers (Columns):")
    print(data.columns.tolist())  # Print column names as a list

    # For illustration, let's plot the first 10 rows of column7 (adjust column name if needed)
    column_name = 'column7'  # Replace with an actual column name from your data

    # Check if the column exists
    if column_name in data.columns:
        # Create a simple line plot for the column
        plt.figure(figsize=(10, 6))
        plt.plot(data[column_name].head(10), marker='o', linestyle='-', color='b')

        # Customize the plot
        plt.title(f'{column_name} Plot')
        plt.xlabel('Index')
        plt.ylabel(column_name)

        # Save the plot to the output directory
        plt.savefig(output_image)
        plt.close()
        print(f"Graph saved as {output_image}")
    else:
        print(f"Column '{column_name}' not found in the data.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize data from HDF5 file and generate a graph.")
    parser.add_argument("--hdf5_file", type=str, required=True, help="Path to input HDF5 file")
    parser.add_argument("--output_image", type=str, required=True, help="Path to output image file")
    
    args = parser.parse_args()
    visualize_data(args.hdf5_file, args.output_image)

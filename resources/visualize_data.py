import argparse
import os
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def visualize_large_parquet(input_parquet, output_dir, bins=50):
    """Process large Parquet file efficiently and generate meaningful visualizations."""
    
    print("Starting data visualization...")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the Parquet file with PyArrow
    print("Loading Parquet file...")
    parquet_file = pq.ParquetFile(input_parquet)

    # Initialize storage for statistics
    column_means = {}
    column_stds = {}
    
    print("Processing data in chunks...")
    for batch in parquet_file.iter_batches(batch_size=100000):  # 100K rows per batch to reduce memory usage
        df = batch.to_pandas()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Select only numeric columns for statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            column_means[col] = column_means.get(col, []) + [df[col].mean()]
            column_stds[col] = column_stds.get(col, []) + [df[col].std()]
    
    print("Aggregating statistics...")
    avg_means = {col: np.nanmean(values) for col, values in column_means.items()}
    avg_stds = {col: np.nanmean(values) for col, values in column_stds.items()}
    
    stats_df = pd.DataFrame({"Mean": avg_means, "Std Dev": avg_stds})
    stats_csv_path = os.path.join(output_dir, 'statistics.csv')
    stats_df.to_csv(stats_csv_path)
    print(f"Saved statistics to {stats_csv_path}")
    
    print("Generating visualizations...")
    full_df = pd.read_parquet(input_parquet)
    full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])
    
    # Average Speed per Car Model
    plt.figure(figsize=(12, 6))
    avg_speed = full_df.groupby('model')['speed_kmh'].mean().sort_values()
    avg_speed.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Average Speed per Car Model')
    plt.xlabel('Car Model')
    plt.ylabel('Speed (km/h)')
    plt.xticks(rotation=45)
    plt.ylim(avg_speed.min() * 0.9, avg_speed.max() * 1.1)  # Adjust y-axis scale
    plt.savefig(os.path.join(output_dir, 'avg_speed_per_model.png'))
    plt.close()
    print("Saved avg_speed_per_model.png")
    
    # Scatter plot of fuel efficiency vs. engine size
    plt.figure(figsize=(10, 6))
    plt.scatter(full_df['engine_size_l'], full_df['fuel_efficiency_l_per_100km'], alpha=0.5, color='red')
    plt.title('Fuel Efficiency vs. Engine Size')
    plt.xlabel('Engine Size (L)')
    plt.ylabel('Fuel Efficiency (L/100km)')
    plt.savefig(os.path.join(output_dir, 'fuel_vs_engine_size.png'))
    plt.close()
    print("Saved fuel_vs_engine_size.png")
    
    # Histogram of RPM distribution
    plt.figure(figsize=(10, 6))
    plt.hist(full_df['rpm'], bins=bins, color='blue', alpha=0.7, edgecolor='black')
    plt.title('RPM Distribution')
    plt.xlabel('RPM')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'rpm_distribution.png'))
    plt.close()
    print("Saved rpm_distribution.png")
    
    # Scatter plot of temperature vs. speed
    plt.figure(figsize=(10, 6))
    plt.scatter(full_df['temperature_c'], full_df['speed_kmh'], alpha=0.5, color='green')
    plt.title('Temperature vs. Speed')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Speed (km/h)')
    plt.savefig(os.path.join(output_dir, 'temp_vs_speed.png'))
    plt.close()
    print("Saved temp_vs_speed.png")
    
    # Correlation heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(full_df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Pairwise Correlation Heatmap')
    plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
    plt.close()
    print("Saved correlation_heatmap.png")
    
    print(f"All visualizations saved in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize large Parquet data efficiently.")
    parser.add_argument("--input_parquet", type=str, required=True, help="Path to input Parquet file")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to output directory for images")
    
    args = parser.parse_args()
    visualize_large_parquet(args.input_parquet, args.output_dir)

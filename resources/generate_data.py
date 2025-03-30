import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_sample_data(output_path, num_rows=7000000):
    """Generate a meaningful dataset with car models and speed measurements."""
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Define sample car brands and models
    car_brands = {
        "Toyota": ["Corolla", "Camry", "RAV4"],
        "Honda": ["Civic", "Accord", "CR-V"],
        "Ford": ["Focus", "Mustang", "Explorer"],
        "BMW": ["3 Series", "5 Series", "X5"],
        "Tesla": ["Model S", "Model 3", "Model X"]
    }
    
    # Generate random data
    data = {
        "timestamp": [(datetime.now() - timedelta(seconds=random.randint(0, 31536000))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_rows)],
        "brand": [random.choice(list(car_brands.keys())) for _ in range(num_rows)],
        "model": [random.choice(car_brands[random.choice(list(car_brands.keys()))]) for _ in range(num_rows)],
        "speed_kmh": np.random.normal(100, 30, num_rows).clip(0, 250),  # Normal distribution around 100 km/h
        "engine_size_l": np.random.choice([1.5, 2.0, 2.5, 3.0, 4.0], num_rows),
        "fuel_efficiency_l_per_100km": np.random.normal(7, 2, num_rows).clip(3, 15),
        "odometer_km": np.random.randint(0, 300000, num_rows),
        "temperature_c": np.random.normal(20, 5, num_rows).clip(-10, 40),
        "rpm": np.random.randint(500, 7000, num_rows),
        "tire_pressure_psi": np.random.normal(32, 3, num_rows).clip(25, 40)
    }
    
    df = pd.DataFrame(data)
    
    # Save the dataframe to Parquet in the output folder
    output_file = os.path.join(output_path, 'data.parquet')
    df.to_parquet(output_file, index=False)
    print(f"Generated sample data and saved to {output_file}")

if __name__ == "__main__":
    output_path = 'output'  # Set output folder
    generate_sample_data(output_path)

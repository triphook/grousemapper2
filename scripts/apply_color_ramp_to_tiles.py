import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from PIL import Image
import os
from google.cloud import storage


def apply_red_to_green_color_ramp(input_folder, output_folder):
    print(input_folder, output_folder)
    in_files = [os.path.join(root, f) for root, _, files in os.walk(input_folder) for f in files if f.endswith(".png")]
    out_files = [f.replace("_tiles_clip", "tiles_clip_rgb") for f in in_files]

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the custom red to green colormap
    # Values are normalized between 0 and 1
    # For a simple red-to-green map, we transition from red at 0 to green at 1
    # Matplotlib's 'RdYlGn_r' (Red-Yellow-Green, reversed) or similar can also be used,
    # but a custom LinearSegmentedColormap gives full control.
    maxval = 1.
    cdict = {
        'red': [(0.0, maxval, maxval),  # Start: Red (1), End: 1 (at 0.0)
                (maxval, 0.0, 0.0)],  # Start: 0 (at 1.0), End: Green (0)
        'green': [(0.0, 0.0, 0.0),  # Start: 0, End: Green (0)
                  (maxval, maxval, maxval)],  # Start: Green (1), End: 1
        'blue': [(0.0, 0.0, 0.0),  # Start: 0, End: 0
                 (maxval, 0.0, 0.0)]  # Start: 0, End: 0
    }
    custom_cmap = matplotlib.colors.LinearSegmentedColormap('RedGreen', cdict)

    # Process all PNG files in the input folder



    for filepath, output_path in zip(in_files, out_files):
        if not os.path.exists(output_path):
            print(output_path)
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            # 1. Open the image in grayscale mode ('L' for luminance)
            try:
                img = Image.open(filepath).convert('L')
            except IOError:
                print(f"Skipping {filepath}, cannot open or convert to grayscale.")
                continue

            img_array = np.array(img)

            # 2. Normalize the image data to the 0-1 range expected by the colormap
            # Avoid division by zero for completely black images
            if img_array.max() == 0:
                normalized_array = img_array
            else:
                normalized_array = img_array / img_array.max()

            # 3. Apply the colormap using matplotlib
            # The result is an RGBA array with values between 0 and 1
            heatmap_array = custom_cmap(normalized_array)

            # 4. Convert the float RGBA array to 8-bit RGB (0-255)
            # Matplotlib outputs values from 0 to 1, we multiply by 255 and cast to uint8
            heatmap_array_uint8 = (heatmap_array[:, :, :3] * 255).astype(np.uint8)  # Keep only RGB channels

            # 5. Convert the NumPy array back to a PIL Image and save
            output_img = Image.fromarray(heatmap_array_uint8, 'RGB')
            output_img.save(output_path)

def upload_directory_to_gcs(local_directory, remote_directory, project_id="utopian-button-361002", bucket_name="grousemapper"):
    storage_client = storage.Client(project_id)
    bucket = storage_client.bucket(bucket_name)
    print(local_directory)
    for root, subdir, files in os.walk(local_directory):
        print(root)
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = f"{remote_directory}/{file}"
            blob = bucket.blob(remote_file)
            print(f"Uploading {local_file} to {remote_file}...")
            blob.upload_from_filename(local_file)


# --- Example Usage ---
# Replace with your actual folder paths
INPUT_DIR = r'C:/Users/jhook/Documents/grousemapper/geo/suitabilitytiles_clip_rgb'
OUTPUT_DIR = r'C:/Users/jhook/Documents/grousemapper/geo/suitability_tiles_clip_rgb'
REMOTE_DIR = r"suitability_tiles_clip_rgb/"

apply_red_to_green_color_ramp(INPUT_DIR, OUTPUT_DIR)
upload_directory_to_gcs(OUTPUT_DIR, REMOTE_DIR, project_id="utopian-button-361002", bucket_name="grousemapper")
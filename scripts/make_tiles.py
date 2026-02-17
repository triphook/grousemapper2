import os
from osgeo import gdal

# gdal2tiles is typically found within the GDAL installation
# You may need to adjust the import mechanism depending on your specific environment setup

# The following import is common for modern GDAL Python bindings
try:
    import gdal2tiles
except ImportError:
    # Fallback for older installations where gdal2tiles was a separate script/module
    # This might require ensuring gdal2tiles.py is in your Python path
    print("gdal2tiles not found as module. Ensure it's accessible in your environment.")
    # A more robust solution for older versions might involve using subprocess as shown in search snippets

def create_web_tiles(input_file, output_folder, tile_size=512, zoom_levels='2-10'):
    """
    Generates web map tiles optimized for OpenLayers using gdal2tiles.

    Args:
        input_file (str): Path to the input large raster file (e.g., a GeoTIFF).
        output_folder (str): Directory for the output tiles and viewer files.
        tile_size (int): Pixel size for the tiles (256 or 512 are standard).
        zoom_levels (str): The range of zoom levels to generate, e.g., '2-10'.
    """
    print(f"Starting tile generation for {input_file}...")
    print(f"Outputting to {output_folder} with tile size {tile_size}px and zoom levels {zoom_levels}")

    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Options dictionary for gdal2tiles
    options = {
        'profile': 'mercator',  # 'mercator' profile is Google Maps compatible (EPSG:3857), standard for web maps
        'resampling': 'average', # 'average' is the default and generally good for speed and quality
        'zoom': zoom_levels,
        'tile_size': tile_size,
        'xyz': True, # Use XYZ tiling scheme (top-to-bottom Y), standard for OpenLayers/Google Maps
        'resume': True # Resume generation if tiles already exist
    }

    try:
        # Call the generate_tiles function
        gdal2tiles.generate_tiles(input_file, output_folder, **options)
        print("Tile generation complete!")
    except Exception as e:
        print(f"An error occurred during tile generation: {e}")
        # In some setups, you might need to use subprocess to call the command-line utility
        # import subprocess
        # subprocess.call(['gdal2tiles.py', '--profile=mercator', f'--tilesize={tile_size}', ...])

# Example Usage
if __name__ == '__main__':
    # Define input and output paths
    # Replace 'your_large_raster.tif' with your actual input file path
    input_raster = r"C:\Users\Jhook\OneDrive - Environmental Protection Agency (EPA)\Desktop\rugr_LC_3\rugrLC_2010_v3.0.tif"
    # Replace 'output_tiles' with your desired output directory name
    output_dir = r"C:\Users\Jhook\OneDrive - Environmental Protection Agency (EPA)\Desktop\output_tiles"

    # Check if the input file exists before running
    if os.path.exists(input_raster):
        # Generate tiles with 512x512 size for better performance
        create_web_tiles(input_raster, output_dir, tile_size=512, zoom_levels='0-12')
    else:
        print(f"Error: Input file not found at {input_raster}. Please update the 'input_raster' variable.")

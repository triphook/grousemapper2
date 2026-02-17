import os
from osgeo_utils.gdal2tiles import main as gdal2tiles
from osgeo import gdal


def create_web_tiles(input_file, tempfile, output_folder, tile_size=512, zoom_levels='2-10'):
    """
    Generates web map tiles optimized for OpenLayers using gdal2tiles.

    Args:
        input_file (str): Path to the input large raster file (e.g., a GeoTIFF).
        output_folder (str): Directory for the output tiles and viewer files.
        tile_size (int): Pixel size for the tiles (256 or 512 are standard).
        zoom_levels (str): The range of zoom levels to generate, e.g., '2-10'.
    """


    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert to 8 bit
    print(f"Converting input file to temporary 8-bit layer")
    ds = gdal.Open(input_file)
    #gdal.Translate('output.tif', ds, options='-of GTiff -co COMPRESS=LZW -projwin 0 0 1000 1000')
    ds = gdal.Translate(tempfile, ds, options=f"-of VRT -ot Byte -scale 0 1 0 100") # scale?
    ds = None

    print(f"Starting tile generation for {input_file}...")
    print(f"Outputting to {output_folder} with tile size {tile_size}px and zoom levels {zoom_levels}")
    options = ["--xyz", "--zoom", zoom_levels, tempfile, output_folder]
    gdal2tiles(options)


# Example Usage
if __name__ == '__main__':
    data_root = r"C:\Users\Jhook\Documents\grousemapper\geo"
    input_raster = os.path.join(data_root, "rugr_LC_3", "rugrLC_2010_v3.0.tif")
    tempfile = os.path.join(data_root, "temp.vrt")
    output_dir = os.path.join(data_root, "output_tiles")

    # Check if the input file exists before running
    if os.path.exists(input_raster):
        # Generate tiles with 512x512 size for better performance
        create_web_tiles(input_raster, tempfile, output_dir)
    else:
        print(f"Error: Input file not found at {input_raster}. Please update the 'input_raster' variable.")

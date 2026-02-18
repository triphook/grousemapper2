from osgeo import gdal
import os

# Allow GDAL to throw Python exceptions
gdal.UseExceptions()


def clip_raster_by_polygon(input_raster_path, input_polygon_path, output_raster_path):
    """
    Clips a raster dataset using a polygon vector layer as a cutline.

    Args:
        input_raster_path (str): Path to the input raster file (e.g., .tif).
        input_polygon_path (str): Path to the input polygon file (e.g., .shp or .gpkg).
        output_raster_path (str): Path for the output clipped raster file.
    """

    print(f"Clipping {input_raster_path} with {input_polygon_path}...")

    # Define the arguments for gdal.Warp()
    # cutlineDSName: Specifies the datasource for the cutline (the polygon file)
    # cropToCutline: Crops the extent of the output dataset to the extent of the cutline
    # dstNodata: Sets the nodata value for pixels outside the cutline (optional, adjust as needed)
    # options: Can include creation options like compression (optional)
    warp_options = gdal.WarpOptions(
        cutlineDSName=input_polygon_path,
        cropToCutline=True,
        # dstNodata=0, # Uncomment to set a specific nodata value
        creationOptions=['COMPRESS=DEFLATE']
    )

    # Perform the warping (clipping) operation
    # The function returns a dataset object, which can be closed to ensure data is written to disk
    clipped_dataset = gdal.Warp(
        output_raster_path,
        input_raster_path,
        options=warp_options
    )

    # Close the dataset
    clipped_dataset = None

    print(f"Successfully clipped raster saved to {output_raster_path}")


if __name__ == "__main__":
    # Example usage:
    # Ensure you replace these paths with your actual file paths
    # The polygon file can be a shapefile (.shp), GeoPackage (.gpkg), etc.

    # Define file names
    input_raster = r"../geo/suitability/rugr_LC_3/rugrLC_2010_v3.0.tif"
    input_polygon = "../geo/wv_boundary.shp"  # or .gpkg, .geojson, etc.
    output_raster = "C:/Users/jhook/Documents/geo/suitability/clipped.tif"

    # Check if input files exist before running
    if os.path.exists(input_raster) and os.path.exists(input_polygon):
        clip_raster_by_polygon(input_raster, input_polygon, output_raster)
    else:
        print("Error: Input raster or polygon file not found")
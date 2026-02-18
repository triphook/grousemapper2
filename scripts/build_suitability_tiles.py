import os
import requests
from osgeo_utils.gdal2tiles import main as gdal2tiles
from osgeo import gdal
import zipfile
from google.cloud import storage


def clip_raster_by_polygon(input_raster_path, input_polygon_path, output_raster_path):
    print(f"Clipping {input_raster_path} with {input_polygon_path}...")
    warp_options = gdal.WarpOptions(
        cutlineDSName=input_polygon_path,
        cropToCutline=True,
        # dstNodata=0, # Uncomment to set a specific nodata value
    )

    clipped_dataset = gdal.Warp(
        output_raster_path,
        input_raster_path,
        options=warp_options
    )
    # Close the dataset
    clipped_dataset = None

    print(f"Successfully clipped raster saved to {output_raster_path}")

def unzip_file(zip_filename, extract_dir):
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Files extracted successfully to: {extract_dir}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def upload_directory_to_gcs(local_directory, project_id="utopian-button-361002", bucket_name="grousemapper"):
    storage_client = storage.Client(project_id)
    bucket = storage_client.bucket(bucket_name)
    for root, subdir, files in os.walk(local_directory):
        remote = root.removeprefix(os.path.dirname(local_directory) + "\\")
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = f"{remote}/{file}".replace("\\", "/")
            blob = bucket.blob(remote_file)
            print(f"Uploading {local_file} to {remote_file}...")
            blob.upload_from_filename(local_file)


def acquire_dataset(url, temp_dir, root_dir):
    local_file = os.path.join(temp_dir, "temp.zip")
    try:
        # Send a GET request to the URL in a streaming fashion to handle large files efficiently
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            with open(local_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # Write file in chunks to manage memory usage
                    if chunk:
                        f.write(chunk)
        print(f"\tDownloaded '{local_file}' successfully. Unzipping...")
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
    unzip_file(local_file, root_dir)
    os.remove(local_file)
    print(f"\tUnzipped to {root_dir}, temporary file {local_file} deleted.")

def create_web_tiles(clipped_r, clipped_8bt, output_folder, tile_size=512, zoom_levels='2-7'):
    # Convert to 8 bit
    ds = gdal.Open(clipped_r)
    # gdal.Translate('output.tif', ds, options='-of GTiff -co COMPRESS=LZW -projwin 0 0 1000 1000')
    ds = gdal.Translate(clipped_8bt, ds, options=f"-of GTiff -ot Byte -scale 0 1 0 100")  # scale?
    ds = None

    # Set 0 as nodata
    ds = gdal.Open(clipped_8bt)
    for i in range(1, ds.RasterCount + 1):
        # set the nodata value of the band
        ds.GetRasterBand(i).SetNoDataValue(0)
    ds = None

    # Generate Tiles
    print(f"Starting tile generation for {clipped_r}. Outputting to {output_folder}...")
    options = ["--xyz", "--zoom", zoom_levels, "-a", 0, clipped_8bt, output_folder]
    gdal2tiles(options)

def main():
    data_root = r"C:\Users\jhook\Documents\grousemapper\geo"

    # Remote path
    dataset_url = r"https://www.sciencebase.gov/catalog/file/get/56d07d9de4b015c306ee988c?f=__disk__c0%2Fd8%2F47%2Fc0d8474b60e01f3e81b2e388b320a14a4dd623f9"

    # Full raster file
    unzipped_path = os.path.join(data_root, "rugr_LC_3", "rugrLC_2010_v3.0.tif")

    # State boundary polygon
    state_polygon = os.path.join(data_root, "wv_boundary.shp")

    # Output
    output_dir = os.path.join(data_root, "suitability_tiles_clip")
    scratch_dir = os.path.join(data_root, "scratch")
    clipped_raster = os.path.join(scratch_dir, "clipped.tif")
    clipped_8bit_raster = os.path.join(scratch_dir, "clipped_8bit3.tif")

    # Create working paths
    for path in scratch_dir, output_dir:
        if not os.path.isdir(path):
            os.makedirs(path)

    print("Downloading suitability raster...")
    #input_raster = acquire_dataset(dataset_url, unzipped_path, scratch_dir, data_root)

    print("Clipping raster to state boundary...")
    #clip_raster_by_polygon(unzipped_path, state_polygon, clipped_raster)

    print("Creating web tiles...")
    create_web_tiles(clipped_raster, clipped_8bit_raster, output_dir)

    print("Uploading web tiles to bucket...")
    #upload_directory_to_gcs(output_dir)


# Example Usage
if __name__ == '__main__':
    main()

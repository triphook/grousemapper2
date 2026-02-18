import pandas as pd
import requests
import json
import os

from google.cloud import storage


def apply_business_rules(layer_name, layer_data):
    if layer_name == 'NPS Lands WV':
        for feature in layer_data["features"]:
            feature['properties']['Source'] = "National Park Service Lands"
            feature['properties']['Category'] = "Fee"
            feature['properties']['Manager'] = "U.S. National Park Service"
            feature['properties']['OwnershipType'] = "Federal"
            feature['properties']['Owner'] = "United States of America"
            feature['properties']['Website'] = "https://nps.gov"
            feature['properties']['Access'] = "Open Access"
    if layer_name == 'NWR USFS Lands':
        for feature in layer_data["features"]:
            feature['properties']['Source'] = "National Wildlife Refuge"
            feature['properties']['OwnershipType'] = "Federal"
            feature['properties']['Owner'] = "United States of America"
            feature['properties']['Website'] = "https://www.fws.gov/program/national-wildlife-refuge-system"
    if layer_name == 'WV State Forest Lands':
        for feature in layer_data["features"]:
            feature['properties']['Source'] = "West Virginia State Forest"
            feature['properties']['OwnershipType'] = "State"
            feature['properties']['Owner'] = "State of West Virginia"
            feature['properties']['Website'] = "https://wvforestry.com/west-virginia-state-forests/"
            feature['properties']['Access'] = "Open Access"
    if layer_name == 'WV State Parks':
        for feature in layer_data["features"]:
            feature['properties']['Source'] = "West Virginia State Park"
            feature['properties']['Manager'] = "WV Division of Natural Resources"
            feature['properties']['Access'] = "Restricted Access"
    if layer_name == 'WVDNR Managed Lands':
        for feature in layer_data["features"]:
            feature['properties']['Source'] = "West Virginia Wildlife Management Area"
            feature['properties']['Website'] = "https://wvdnr.gov/"
    if layer_name == 'WVDNR Managed Lands':
        for feature in layer_data["features"]:
            feature['properties']['Source'] = "West Virginia Wildlife Management Area"
            feature['properties']['Website'] = "https://wvdnr.gov/"
    else:
        print(layer_name)

    return layer_data

def clean_schema(layer_name, layer_data, boundary_schema):
    schema_dict = dict(boundary_schema[boundary_schema.Layer == layer_name][['Field', 'Rename']].values)
    for feature in layer_data['features']:
        old_fields = list(feature['properties'].keys())
        for old_field in old_fields:
            try:
                new_field = schema_dict[old_field]
                feature['properties']['Dataset'] = layer_name
                feature['properties'][new_field] = feature['properties'].pop(old_field)
            except KeyError:
                del feature['properties'][old_field]
    return layer_data


def query_features(url):
    query_params = {
        "where": "1=1",  # A common way to return all records (adjust as needed)
        "outFields": "*",  # Return all fields
        "f": "geojson",  # Request GeoJSON format for easy parsing (or "json" for ESRI JSON)
        "returnGeometry": True
    }
    query_response = requests.get(f"{url}/query", params=query_params)
    if query_response.status_code == 200:
        return query_response.json()
    else:
        print(f"Failed to query layer {url}: {query_response.status_code}")
        return None


def write_to_file(geojson_data, output_file):
    # Open the file in write mode and dump the data
    with open(output_file, "w") as f:
        # Use json.dump() to write the dictionary to the file
        # indent=4 makes the file human-readable and formatted
        json.dump(geojson_data, f, indent=4)
    print(f"Successfully wrote GeoJSON data to {output_file}")


def upload_to_gcs(local_file, remote_file, project_id="utopian-button-361002", bucket_name="grousemapper"):
    storage_client = storage.Client(project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(remote_file)
    print(f"Uploading {local_file} to {remote_file}...")
    blob.upload_from_filename(local_file)


def main():
    feature_server_url = "https://services6.arcgis.com/cGI8zn9Oo7U9dF6z/arcgis/rest/services/WV_Public_Lands_pro/FeatureServer"
    boundary_schema_path = "boundary_schema_2.csv"
    bucket_folder = "clean_boundaries_2"
    local_dir = "../geo/clean_boundaries_2"

    boundary_schema = pd.read_csv(boundary_schema_path)

    response = requests.get(f"{feature_server_url}?f=json")
    service_metadata = response.json()

    for layer_info in service_metadata.get("layers", []):
        layer_id = layer_info.get("id")
        layer_name = layer_info.get("name")

        # You can then construct the URL for the specific layer
        layer_url = f"{feature_server_url}/{layer_id}"

        # Perform further operations on the layer, e.g., query features
        layer_data = query_features(layer_url)

        # Clean the schema
        cleaned = clean_schema(layer_name, layer_data, boundary_schema)

        # Apply business rules
        cleaned = apply_business_rules(layer_name, cleaned)

        # Write to file and upload to bucket
        local_outfile = os.path.join(local_dir, f"{layer_name}.geojson")
        remote_outfile = f"{bucket_folder}/{layer_name}.geojson"
        write_to_file(cleaned, local_outfile)
        upload_to_gcs(local_outfile, remote_outfile)


if __name__ == "__main__":
    main()

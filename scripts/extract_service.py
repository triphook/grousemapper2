import requests
import json


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



def main():
    feature_server_url = "https://services6.arcgis.com/cGI8zn9Oo7U9dF6z/arcgis/rest/services/WV_Public_Lands/FeatureServer"
    response = requests.get(f"{feature_server_url}?f=json")
    service_metadata = response.json()
    all_cats = set()
    for layer_info in service_metadata.get("layers", []):
        print(all_cats)
        layer_id = layer_info.get("id")
        layer_name = layer_info.get("name")

        # You can then construct the URL for the specific layer
        layer_url = f"{feature_server_url}/{layer_id}"

        # Perform further operations on the layer, e.g., query features
        layer_data = query_features(layer_url)
        if layer_data:
            print(f"{layer_id}, {layer_name}")
            for feature in layer_data['features']:
                try:
                    if feature['properties']['Category'] == 'Other':
                        print(feature['properties'])
                except KeyError:
                    continue



if __name__ == "__main__":
    main()

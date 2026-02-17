from google.cloud import storage

def authenticate_implicit_with_adc(project_id):
    """
    Lists the buckets in the project using Application Default Credentials.
    The client library will automatically find the credentials.
    """
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(f"* {bucket.name}")
    print("Listed all storage buckets.")

# Replace "your-google-cloud-project-id" with your actual project ID
authenticate_implicit_with_adc("utopian-button-361002")
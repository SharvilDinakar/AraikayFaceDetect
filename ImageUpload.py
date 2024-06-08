import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

# Replace with your connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=imagebucket;AccountKey=VVBACkgQEaAtNMaHaDIwPl6cEpvVxmCNo1ZQmWh+kJav1E8U1Dtidq5ENY9zVTyX/IVNGA379LH1+ASttXix4g==;EndpointSuffix=core.windows.net"

# Container name (change if needed)
container_name = "visitors"

# Local folder path (replace with your folder path)
local_folder_path = "/Users/sharvildinakar/Documents/face/"

def upload_images_to_blob(connection_string, container_name, local_folder_path):
    """
    Uploads all images from a local folder to an Azure blob storage container.

    Args:
        connection_string (str): Azure storage connection string.
        container_name (str): Name of the blob storage container.
        local_folder_path (str): Path to the local folder containing images.
    """
    try:
        # Create BlobServiceClient from the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get container client
        container_client = blob_service_client.get_container_client(container_name)

        # List all files in the local folder
        for filename in os.listdir(local_folder_path):
            # Extract parentID from the filename
            parent_id = filename.split('-')[0]

            # Construct the full local file path
            local_file_path = os.path.join(local_folder_path, filename)

            # Construct the blob name (including the parentID folder)
            blob_name = f"{parent_id}/{filename}"

            # Get the blob client
            blob_client = container_client.get_blob_client(blob_name)

            try:
                # Upload the image with open in binary mode (rb)
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data)
            except ResourceExistsError:
                print(f"Image '{filename}' is already uploaded to container '{container_name}'!")
                os.remove(local_file_path)
            else:
                print(f"Image '{filename}' uploaded successfully to container '{container_name}'!")

                # Delete the local file after successful upload
                os.remove(local_file_path)
                print(f"Local file '{filename}' deleted successfully!")

    except Exception as ex:
        print(f"Error uploading images: {ex}")

if __name__ == "__main__":
    # Ensure you have replaced placeholders with your information
    upload_images_to_blob(connection_string, container_name, local_folder_path)


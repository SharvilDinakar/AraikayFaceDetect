import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError


class AzureBlobUploader:
    def __init__(self, connection_string, container_name, local_folder_path):
        self.connection_string = connection_string
        self.container_name = container_name
        self.local_folder_path = local_folder_path
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        self.logger = logging.getLogger(__name__)

    def upload_images(self):
        try:
            for filename in os.listdir(self.local_folder_path):
                parent_id = filename.split('-')[0]
                local_file_path = os.path.join(self.local_folder_path, filename)
                blob_name = f"{parent_id}/{filename}"
                blob_client = self.container_client.get_blob_client(blob_name)

                try:
                    with open(local_file_path, "rb") as data:
                        blob_client.upload_blob(data)
                except ResourceExistsError:
                    self.logger.error(f"Image '{filename}' is already uploaded to container '{self.container_name}'!")
                    os.remove(local_file_path)
                else:
                    self.logger.info(f"Image '{filename}' uploaded successfully to container '{self.container_name}'!")
                    os.remove(local_file_path)
                    self.logger.info(f"Local file '{filename}' deleted successfully!")

        except Exception as ex:
            self.logger.error(f"Error uploading images: {ex}")

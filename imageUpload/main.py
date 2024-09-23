from config_loader import connection_string, container_name, local_folder_path
from azure_blob import AzureBlobUploader

def main():
    uploader = AzureBlobUploader(connection_string, container_name, local_folder_path)
    uploader.upload_images()

if __name__ == "__main__":
    main()

import os
import re
import time
import requests
import json
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient

# Replace with your values
prediction_key = "9a7da1a1a9844330bbb8ae556d5c3061"

#https://<your-resource-name>.cognitiveservices.azure.com/customvision/v3.0/Prediction/<project-id>/detect/iterations/<iteration-name>/image
#Sharvils Endpoint
#endpoint = "https://araikayfacerecognition-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/12a7f579-dbce-4dd6-bfb4-b63b54bef6bc/detect/iterations/Iteration1/image"

#Araikay Endpoint
endpoint = "https://araikaycustomfacerecognition-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/edbb6598-fe4b-4a9d-8a16-8bc108b54437/detect/iterations/Iteration1/image"

#iteration_id = "9401c380-4817-4ea9-924f-709ac4002d70"
#New Iteration ID
iteration_id="b25abe24-f4d8-4964-9894-7678dbd9818e"

connection_string = "DefaultEndpointsProtocol=https;AccountName=imagebucket;AccountKey=VVBACkgQEaAtNMaHaDIwPl6cEpvVxmCNo1ZQmWh+kJav1E8U1Dtidq5ENY9zVTyX/IVNGA379LH1+ASttXix4g==;EndpointSuffix=core.windows.net"
container_name = "visitors"

# Corrected regular expression to extract parentID and timestamp from filename
filename_pattern = re.compile(r"(\d+)/\d+-face_detect(\d{8})(\d{4})")

def extract_info(blob_name):
    """
    Extracts the timestamp and parentID from the blob name.

    Args:
        blob_name (str): Name of the blob.

    Returns:
        tuple: A tuple containing parentID and formatted timestamp, or (None, None) if the pattern does not match.
    """
    match = filename_pattern.match(blob_name)
    if match:
        parent_id = match.group(1)
        date_str = match.group(2)  # YYYYMMDD
        time_str = match.group(3)  # HHMM
        # Combine date and time
        timestamp_str = f"{date_str}{time_str}"
        # Convert to datetime object
        timestamp = datetime.strptime(timestamp_str, "%Y%m%d%H%M")
        # Format datetime object
        formatted_timestamp = timestamp.strftime("%H:%M, %d/%m/%Y")
        return parent_id, formatted_timestamp
    return None, None

def send_image_for_prediction(blob_client, result_map):
    """
    Downloads an image from Azure Blob Storage and sends it for prediction using the Custom Vision Prediction API.

    Args:
        blob_client: Azure BlobClient object representing the image blob.
        result_map (dict): Dictionary to store tag details (tag, probability, parentID, timestamp).
    """
    try:
        # Download image data
        image_data = blob_client.download_blob().readall()

        # Prepare request headers
        headers = {
            "Prediction-Key": prediction_key,
            "Content-Type": "application/octet-stream"
        }

        # Send prediction request
        response = requests.post(endpoint, headers=headers, data=image_data)

        if response.status_code == 200:
            predictions = response.json()["predictions"]  # Extract predictions array

            # Access prediction details of the first image
            if predictions:
                first_prediction = predictions[0]
                tag_name = first_prediction.get("tagName", "Unknown")  # Get tagName or default to "Unknown"
                probability = first_prediction.get("probability", 0.0)  # Get probability or default to 0.0

                # Extract parentID and timestamp from the blob name
                parent_id, timestamp = extract_info(blob_client.blob_name)

                # Store result in the result_map
                result_map[blob_client.blob_name] = {
                    "tag": tag_name,
                    "probability": probability,
                    "parentID": parent_id,
                    "timestamp": timestamp
                }

                # Print details of the prediction along with parentID and timestamp
                print(f"Image: {blob_client.blob_name}")
                print(f"\tTag: {tag_name}, Probability: {probability:.2f}, ParentID: {parent_id}, Timestamp: {timestamp}")
            else:
                print(f"No predictions for image: {blob_client.blob_name}")

        else:
            print(f"Error: {response.status_code} for image: {blob_client.blob_name}")

    except Exception as e:
        print(f"Error processing blob with Custom Vision:", e)

def process_new_blobs(blob_service_client, container_client, last_check_time, result_map):
    """
    Processes new blobs uploaded after the last check time.

    Args:
        blob_service_client: Azure BlobServiceClient object.
        container_client: Azure BlobContainerClient object.
        last_check_time (datetime): Last time the new blobs were checked.
        result_map (dict): Dictionary to store tag details (tag, probability, parentID, timestamp).
    """
    # List blobs in the container
    for blob in container_client.list_blobs():
        # Only process image blobs
        if blob.name.lower().endswith((".jpg", ".jpeg", ".png")) and blob.last_modified.replace(tzinfo=timezone.utc) > last_check_time:
            blob_client = container_client.get_blob_client(blob)
            send_image_for_prediction(blob_client, result_map)
            print("\n")  # Add a newline between image predictions

def main():
    # Dictionary to store tag details (tag, probability, parentID, timestamp)
    result_map = {}

    # Create BlobServiceClient from the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get container client
    container_client = blob_service_client.get_container_client(container_name)

    # Initialize last_check_time to current time
    last_check_time = datetime.now(timezone.utc)

    # Main loop
    while True:
        # Process new blobs uploaded after the last check time
        process_new_blobs(blob_service_client, container_client, last_check_time, result_map)
        
        # Update last_check_time to current time
        last_check_time = datetime.now(timezone.utc)

        # Sleep for 1 minute before checking for new blobs again
        time.sleep(60)

if __name__ == "__main__":
    main()


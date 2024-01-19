from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime

class ConnectToBlob:
    def __init__(self)-> None:
        connection_string = "DefaultEndpointsProtocol=https;AccountName=wiredetailsstorage;AccountKey=iN1eHEwUMftFPKPNuwvmpWE5hYm+LzUEh5u1MdfanyeipTw9zE1AA4KFoKwZfqoACJvoRVXB9jzb+ASttSA6zQ==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name="transactionfilescontainer"
        self.container_client = blob_service_client.get_container_client(container_name)

    def upload_file_to_blob(self, wire_details: list) -> bool:
        file_name = self.file_name()

        try:
            # Open the file in binary write mode
            with open(file_name, "wb") as file:
                for transaction_record in wire_details:
                    # Ensure transaction_record is a string
                    record_str = str(transaction_record)
                    file.write(record_str.encode()) # Encode the string to bytes before writing

            # Upload the file to Azure Blob Storage
            blob_client = self.container_client.get_blob_client(file_name)
            with open(file_name, "rb") as data:
                blob_client.upload_blob(data)

            return True # Return True to indicate successful upload

        except Exception as e:
            print(f"An error occurred during file upload: {e}")
            return False # Return False to indicate upload failure
    
    def file_name(self):
        current_datetime = datetime.now()
        # Format the date and time into a string separated by underscore
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f"Wire_Transaction_Details_{formatted_datetime}.txt"  # Add .txt extension for a file name
        return file_name


        

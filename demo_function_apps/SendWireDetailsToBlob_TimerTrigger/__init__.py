import sys
sys.path.insert(3,"C:/Users/faisa/OneDrive/Desktop/Banking Application/Model")
sys.path.insert(3,"C:/Users/faisa/OneDrive/Desktop/Banking Application/helpers")

import datetime
import logging
import azure.functions as func
from wire_transaction_details_model import DatabaseManager
from ConnectToBlob import ConnectToBlob

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')


    database_manager=DatabaseManager()
    records_from_wire_transaction_detail_table=database_manager.fetch_records_from_table()
    
    if ConnectToBlob().upload_file_to_blob(records_from_wire_transaction_detail_table):
        print("Successfully uploaded to blob")
    else:
        print("Upload Failed")

import sys
sys.path.insert(2,"C:/Users/faisa/OneDrive/Desktop/Banking Application/Model")

import logging
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import azure.functions as func
from wire_transaction_details_model import DatabaseManager


def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "POST":
        
        request_token=req.headers.get('Authorization')
        try:
            servicebus_namespace = "transactionsBusTrigger"
            queue_name = "transactions_queue"
            sas_connection_string = "Endpoint=sb://transactionsbustrigger.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ncsZO2wKPgArXX07bEqlQ1Kd4cGcxrkHg+ASbHRqmQA="

            req_body = req.get_json()

            if req_body:
                transaction_id = req_body.get("transaction_id")
                sender_name = req_body.get("sender_name")
                receiver_name = req_body.get("receiver_name")
                amount = req_body.get("amount")
                date = req_body.get("date")  
                transaction_status = req_body.get("transaction_status")  
                currency = req_body.get("currency")  
                description = req_body.get("description")  
                reference_number = req_body.get("reference_number")  


                if sender_name and receiver_name and transaction_id and amount:            
                    
                    #inserting into the postgres table 
                    db=DatabaseManager()
                    add_to_db=db.add_records_to_transaction_table(transaction_id=transaction_id,sender_name=sender_name,receiver_name=receiver_name,amount=amount,date=date,transaction_status=transaction_status,currency=currency,description=description,reference_number=reference_number)

                    if add_to_db:
                        logging.info("Sucessfully posted to db")
                    else:
                        logging.info("Not posted to DBj")
                    

                    result = {
                        "TRANSACTION ID": transaction_id,
                        "SENDER NAME": sender_name,
                        "RECEIVER NAME": receiver_name,
                        "AMOUNT": amount,
                        "DATE": date,
                        "TRANSACTION STATUS": transaction_status,
                        "CURRENCY": currency,
                        "DESCRIPTION": description,
                        "REFERENCE NUMBER": reference_number
                    }

                    # Create a ServiceBusClient using the SAS connection string
                    servicebus_client = ServiceBusClient.from_connection_string(sas_connection_string)

                    # Create a sender for the queue
                    sender = servicebus_client.get_queue_sender(queue_name=queue_name)

                    with sender:
                        # Create a ServiceBusMessage with the JSON content
                        json_string = json.dumps(result)
                        message = ServiceBusMessage(body=json_string.encode('utf-8'))

                        # Send the message to the queue
                        sender.send_messages(message)

                    logging.info(result)

                    return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")
                else:
                    # Handle missing or invalid parameters
                    return func.HttpResponse("Invalid or incomplete request data", status_code=400)

        except Exception as e:
            # Log the exception and return a 500 status code
            logging.exception(f"Error processing request: {str(e)}")
            return func.HttpResponse("Internal Server Error", status_code=500)

    return func.HttpResponse("Invalid request method", status_code=405)

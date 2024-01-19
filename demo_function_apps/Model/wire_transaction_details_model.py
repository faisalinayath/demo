import sys
sys.path.insert(1,"C:/Users/faisa/OneDrive/Desktop/Banking Application/db_credentials")

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from  wire_transaction_connection import WireTransactionDbConnection



Base = declarative_base()

class WireTransactionModel(Base):
   __tablename__ = "WireTransactionDetails"

   transaction_id = Column("transaction_id", Integer, primary_key=True)
   sender_name = Column("sender_name", String)
   receiver_name = Column("receiver_name", String)
   amount = Column("amount", String)
   date = Column("date", String)
   transaction_status = Column("transaction_status", String)
   currency = Column("currency", String)
   description = Column("description", String)
   reference_number = Column("reference_number", String)

   def __init__(self, transaction_id, sender_name, receiver_name, amount, date, transaction_status, currency, description, reference_number):
       self.transaction_id = transaction_id
       self.sender_name = sender_name
       self.receiver_name = receiver_name
       self.amount = amount
       self.date = date
       self.transaction_status = transaction_status
       self.currency = currency
       self.description = description
       self.reference_number = reference_number

   def __repr__(self):
       return f"({self.transaction_id}{self.sender_name}{self.receiver_name}{self.amount}{self.date}{self.transaction_status}{self.currency}{self.description}{self.reference_number})"


class DatabaseManager:
    def __init__(self):
        db_conn = WireTransactionDbConnection()
        connection_string = db_conn.initialize_connection_string()
        engine = create_engine(connection_string)
        self.engine = engine

    def create_columns(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def add_records_to_transaction_table(self, transaction_id, sender_name, receiver_name, amount, date, transaction_status, currency, description, reference_number):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            try:
                transaction_detail = WireTransactionModel(
                    transaction_id=transaction_id,
                    sender_name=sender_name,
                    receiver_name=receiver_name,
                    amount=amount,
                    date=date,
                    transaction_status=transaction_status,
                    currency=currency,
                    description=description,
                    reference_number=reference_number
                )
                session.add(transaction_detail)
                session.commit()
                return True  # Return True to indicate success
            except Exception as e:
                session.rollback()  # Rollback the session in case of an error
                print(f"An error occurred: {e}")
                return False  # Return False to indicate failure
            
    def fetch_records_from_table(self) -> list:
        Session=sessionmaker(bind=self.engine)
        session=Session()

        records_from_wire_transaction_detail_table=[i for i in session.query(WireTransactionModel)]
        return records_from_wire_transaction_detail_table










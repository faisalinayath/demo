
class WireTransactionDbConnection:    
    def __init__(self):
        self.username='postgres'
        self.password='Fai2001#'
        self.host='localhost'
        self.port='5432'
        self.database='WIRE_TRANSACTION'
        
    def initialize_connection_string(self):
        connection_string=f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        return connection_string
    
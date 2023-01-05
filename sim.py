import schema
from DB_class import DynamoDB_con

words = [
    
    ]

DB =  DynamoDB_con()

for w in words:
    DB.send_data(w,'TB_JumbledWord_bank')
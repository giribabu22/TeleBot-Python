import boto3,os
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
load_dotenv()

print('dynamodb connected!!....')

dynamodb = boto3.resource( service_name = os.getenv('service_name'),region_name = os.getenv('region_name'),aws_access_key_id = os.getenv('aws_access_key_id'), aws_secret_access_key = os.getenv('aws_secret_access_key'))
existing_tables = [table.name for table in dynamodb.tables.all()]
# print(existing_tables)
if 'Demo_' not in existing_tables:  
    dynamodb.create_table(
        TableName='Demo_',
        KeySchema=[
            {
                'AttributeName': 'Demo_Id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Id',
                'KeyType': 'RANGE'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Demo_Id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Id',
                'AttributeType': 'S'
            }
            
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  
        }
    )
    print('create table Demo_')
if 'TB_JumbledWord_Engagement' not in existing_tables:  
    dynamodb.create_table(
        TableName='TB_JumbledWord_Engagement',
        KeySchema=[
            {
                'AttributeName': 'JumbledWord_InitiatedByUser_ID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'JumbledWord_InitiatedByUser_ID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  
        }
    )
    print('create table JumbledWord_Engagement')
    
if "TB_User_Master" not in existing_tables:
    dynamodb.create_table(
        TableName='TB_User_Master',
        KeySchema=[
            {
                'AttributeName': 'User_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  
        }
    )
    print('create table User_Master')

if "TB_User_Points" not in existing_tables:
    dynamodb.create_table(
        TableName='TB_User_Points',
        KeySchema=[
            {
                'AttributeName': 'User_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  
        }
    )
    print('create table User_Points')
    
if "TB_Telegram_Master" not in existing_tables:
    dynamodb.create_table(
        TableName='TB_Telegram_Master',
        KeySchema=[
            {
                'AttributeName': 'User_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  
        }
    ) 
    print("Table status: Telegram_Master")

if "TB_Quiz_Engagement" not in existing_tables:
    dynamodb.create_table(
        TableName='TB_Quiz_Engagement',
        KeySchema=[
            {
                'AttributeName': 'User_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  
        }
    )
    print('create table Quiz_Engagement')
# print('Hello Temp_JumbledWord_Session table id. we need for that we need to generate the Id!! you need to genarate the id.!!!!!!!!!!!!')
if "TB_Temp_JumbledWord_Session" not in existing_tables:
    dynamodb.create_table(
        TableName='TB_Temp_JumbledWord_Session',
        KeySchema=[
            {
                'AttributeName': 'Id',
                'KeyType': 'HASH'  
            }
        ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
if "TB_JumbledWord_bank" not in existing_tables:
    dynamodb.create_table(
        TableName='TB_JumbledWord_bank',
        KeySchema=[
            {
                'AttributeName': 'word',
                'KeyType': 'HASH'  
            }
        ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'word',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
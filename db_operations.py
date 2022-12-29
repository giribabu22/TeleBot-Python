# from pymongo import MongoClient
import datetime
import config  # 
import playerData

client = MongoClient(config.MONGO_CLIENT_KEY)
db = client.get_database('jumble_db')
# collections
jumble_engagement = db.jumble_engagement
temp_session = db.temp_jumble_session
user_points = db.user_points

def post_data(data, col_name):
    
    if type(data) == dict:
        if col_name == 'user_points':
            res = user_points.insert_one(data)
            print('inserted one in user_points \n', res)
            
        elif col_name == 'jumble_engagement':
            res = jumble_engagement.insert_one(data)
            print('inserted one in jumble_engagement \n', res)
            
        elif col_name == 'temp_session':
            res = temp_session.insert_one(data)
            print('inserted one in temp_session \n', res)
        
    elif type(data) == list:
        if col_name == 'user_points':
            res = user_points.insert_many(data)
            print('inserted many in user_points \n', res)
            
        elif col_name == 'jumble_engagement':
            res = jumble_engagement.insert_many(data)
            print('inserted many in jumble_engagement \n', res)
            
        elif col_name == 'temp_session':
            res = temp_session.insert_many(data)
            print('inserted many in jumble_engagement \n', res)
        
# def get_data(data, col_name): 
#     if type(data) == dict:
#         if col_name == 'user_points':
#             res = user_points.insert_one(data)
#             print('inserted one in user_points \n', res)
            
#         elif col_name == 'jumble_engagement':
#             res = jumble_engagement.insert_one(data)
#             print('inserted one in jumble_engagement \n', res)
            
#         elif col_name == 'temp_session':
#             res = temp_session.insert_one(data)
#             print('inserted one in temp_session \n', res)


data = {
    "user_id": "68346257",
    "date": datetime.datetime.now(),
    "points": 10
}

# a = user_points.insert_one(data)
# a = post_data(playerData.players, 'user_points')
# print(a)
# print(playerData.players)
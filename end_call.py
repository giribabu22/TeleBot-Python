from DB_class import DynamoDB_con

import datetime

DB = DynamoDB_con()

sessionData,totalSess = DB.read_read('TB_Temp_JumbledWord_Session')
EngagementData,totalEnga = DB.read_read('TB_JumbledWord_Engagement')
print(sessionData,EngagementData)
def UpdateTheData():
    print('sessionData: ',sessionData)
    print('EngagementData:',EngagementData)
    total_sum_points = {}
    for dic in sessionData:
        if dic['User_Id'] not in total_sum_points:
            total_sum_points[dic['User_Id']] =  {'Points_Scored':dic["Points_Scored"],'Datetime':dic['Datetime']}
        else:
            total_sum_points[dic['User_Id']]['Points_Scored'] +=  dic["Points_Scored"]

    for dic in total_sum_points:
        print(str(total_sum_points[dic]['Points_Scored']))
        data = {"User_id":str(dic),"date": str(datetime.datetime.now()),"JumbledWord_Points":str(total_sum_points[dic]['Points_Scored']),"JumbledWord_Participation":"None"}
        DB.send_data(data,'TB_User_Points')
        
# UpdateTheData()
# d,l = DB.read_read('TB_User_Points')
# print(d)
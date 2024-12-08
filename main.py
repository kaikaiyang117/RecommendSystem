import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "packageClass")))

from fastapi import Header, Cookie
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
from packageClass.DataBase import Neo4jDatabase
from packageClass.User import User
from packageClass.Activity import Activity


db = Neo4jDatabase(uri="bolt://localhost:7687", username="neo4j", password="kkykkykky")

app = FastAPI()

@app.get("/")
def read_root():
    userInfoFile = "/home/kky/RecommendSystem/packageClass/Recommend_info/user_info.csv"
    db.import_users_from_csv_alternatively(userInfoFile)
    activityInfoUser = "/home/kky/RecommendSystem/packageClass/Recommend_info/activity_info.csv"
    db.import_activities_from_csv(activityInfoUser)
    db.close()


# 查询对应user的信息 user：name return json
@app.get("/user/{name_id}")
def getUserInfo(name_id:str):
    user_data = db.query_user_by_id(name_id)
    return user_data


# user：name return json
@app.get("/activity/{activity_id}")
def getActivityInfo(activity_id:int):
    activity_data = db.query_activity_by_id(activity_id)
    return activity_data       


# @app.get("/recommand/{name_id}")
# def recommandAcitivity(name_id:str):    
#     #TODO 完成推荐函数

#     return 

@app.get("/joinOrQuit/{activity_id}{user_id}")
def joinOrQuit():
    Isjoin = True
    
    if not Isjoin:
        status = "not join"
    else:
        status = "Cancel join"
    return{
        "status": status
    }


@app.get("/Collection/{activity_id}{user_id}")
def joinOrQuit():
    IsLike = True
    
    if not IsLike:
        status = "Cancel Like"
    else:
        status = "Has Like"
    return{
        "status": status
    }

@app.get("/deleteAllDate/")
def deleteData():
    db.clear_all_data()
    return {"statua": "success"}

@app.get("/hasJoins/{user_id}")
def read_has_join(user_id:str):
    activityIds = [1,2,3,4,5,6,7]
    ActivityInfos =[]
    
    for i in activityIds:
        activity = db.query_activity_by_id(i)
        ActivityInfos.append(activity)

    return ActivityInfos


@app.get("/hasLikes/{user_id}")
def read_has_join(user_id:str):
    activityIds = [1,2,3,4,5,6,7]
    ActivityInfos =[]
    
    for i in activityIds:
        activity = db.query_activity_by_id(i)
        ActivityInfos.append(activity)

    return ActivityInfos



@app.get("/hasPublish/{user_id}")
def read_has_join(user_id:str):
    activityIds = [1,2,3,4,5,6,7]
    ActivityInfos =[]
    
    for i in activityIds:
        activity = db.query_activity_by_id(i)
        ActivityInfos.append(activity)

    return ActivityInfos


@app.get("/recommand/{user_id}")
def read_has_join(user_id:str):
    activityIds = [1,2,3,4,5,6,7]
    ActivityInfos =[]
    
    for i in activityIds:
        activity = db.query_activity_by_id(i)
        ActivityInfos.append(activity)

    return ActivityInfos

# 添加活动

# 通过csv导入neo4j数据库信息

# 为推荐推荐合适信息 user：name return list[json]
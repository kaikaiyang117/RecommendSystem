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

@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User-Agent": user_agent, "Session-Token": session_token}


# 查询对应user的信息 user：name return json
@app.get("/user/{name_id}")
def getUserInfo(name_id:str):
    user_data = db.read_user_node(user_id=name_id)
    # print(user_data[1]["name"])
    if len(user_data) == 1 :
        return user_data[0]
    elif len(user_data) > 1:
        raise HTTPException(status_code=404, detail="result not only")
    else:
        raise HTTPException(status_code=404, detail="not have result")

# 查询activaity信息 
# user：name return json

@app.get("/activity/{activity_id}")
def getActivityInfo(activity_id:str):
    activity_data = db.read_activity_node(activity_id=activity_id)
    # print(user_data[1]["name"])
    if len(activity_data) == 1 :
        return activity_data[0]
    elif len(activity_data) > 1:
        raise HTTPException(status_code=404, detail="result not only")
    else:
        raise HTTPException(status_code=404, detail="not have result")


@app.get("/recommand/{name_id}")
def recommandAcitivity(name_id:str):    
    #TODO 完成推荐函数

    return 

@app.get("/deleteAllDate/")
def deleteData():
    db.clear_all_data()

    return {"statua": "success"}

# 添加活动

# 通过csv导入neo4j数据库信息

# 为推荐推荐合适信息 user：name return list[json]
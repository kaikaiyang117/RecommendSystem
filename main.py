from fastapi import Header, Cookie
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from packageClass.DataBase import Neo4jDatabase



app = FastAPI()

@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User-Agent": user_agent, "Session-Token": session_token}

@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/items/")


# 查询对应user的信息 user：name return json

# 查询activaity信息 user：name return json

# 添加用户

# 添加活动

# 通过csv导入neo4j数据库信息

# 为推荐推荐合适信息 user：name return list[json]
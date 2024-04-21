import uvicorn as uvicorn
import multiprocessing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config
from app.db.init import init_db, update_db, init_super_user

from app.core.config import settings

# App
App = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f"{settings.API_V1_STR}/openapi.json")

# 跨域
App.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# uvicorn服务
Server = uvicorn.Server(Config(App, host=settings.HOST, port=settings.PORT,
                               reload=settings.DEV, workers=multiprocessing.cpu_count()))


def init_routers():
    """
    初始化路由
    """
    from app.api.apiv1 import api_router
    # API路由
    App.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':

    # 初始化路由
    init_routers()

    # 初始化数据库
    init_db()

    # 更新数据库
    update_db()

    # 初始化超级管理员
    #init_super_user()

    # 启动API服务
    Server.run()
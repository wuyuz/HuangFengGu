import secrets
from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    # 项目名称
    PROJECT_NAME = "HFG"
    # API路径
    API_V1_STR: str = "/api/v1"

    # 密钥
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 允许的域名
    ALLOWED_HOSTS: list = ["*"]

     # TOKEN过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 时区
    TZ: str = "Asia/Shanghai"
    # API监听地址
    HOST: str = "0.0.0.0"
    # API监听端口
    PORT: int = 3001
    # 前端监听端口
    NGINX_PORT: int = 3000
    # 是否调试模式
    DEBUG: bool = False
    # 是否开发模式
    DEV: bool = False
    # 配置文件目录
    CONFIG_DIR: Optional[str] = None
    # 超级管理员
    SUPERUSER: str = "admin"  # MmQwoi4RCmuJeVKx

    @property
    def ROOT_PATH(self):
        return Path(__file__).parents[2]

    @property
    def LOG_PATH(self):
        return self.CONFIG_PATH / "logs"

    @property
    def CONFIG_PATH(self):
        if self.CONFIG_DIR:
            return Path(self.CONFIG_DIR)
        return self.ROOT_PATH / "config"


settings = Settings(
    _env_file=Settings().CONFIG_PATH / "app.env",
    _env_file_encoding="utf-8"
)

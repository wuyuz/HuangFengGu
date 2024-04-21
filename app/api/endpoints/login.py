from typing import Any
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Form
from app.db import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.log import logger
from app import schemas
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/access-token", summary="获取token", response_model=schemas.Token)
async def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    otp_password: str = Form(None)
) -> Any:
    """
    获取认证Token
    """
    # 检查数据库
    success, user = User.authenticate(
        db=db,
        name=form_data.username,
        password=form_data.password,
        otp_password=otp_password
    )
    if not success:
        # 认证不成功
        logger.warn(f"用户 {user.name} 登录失败！")
        raise HTTPException(status_code=401, detail="用户名、密码或二次校验码不正确")
    elif user and not user.is_active:
        raise HTTPException(status_code=403, detail="用户未启用")
    logger.info(f"用户 {user.name} 登录成功！")
    return schemas.Token(
        access_token=security.create_access_token(
            userid=user.id,
            username=user.name,
            super_user=user.is_superuser,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        token_type="bearer",
        super_user=user.is_superuser,
        user_name=user.name,
        avatar=user.avatar
    )

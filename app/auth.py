# from datetime import datetime, timedelta
# from typing import Optional
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from sqlmodel.ext.asyncio.session import AsyncSession
# from models import User
# from database import get_session
# from typing import Dict, Any
# import os

# # 安全配置
# SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时

# # 密码处理
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # OAuth2配置
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


# async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
#     from sqlmodel import select

#     result = await session.execute(select(User).where(User.email == email))
#     return result.scalar_one_or_none()


# async def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[User]:
#     user = await get_user_by_email(email, session)
#     if not user:
#         return None
#     if not verify_password(password, user.password_hash):
#         return None
#     return user


# def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = await get_user_by_email(email, session)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
#     if not current_user.is_superuser and current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return current_user


# async def get_current_judge_user(current_user: User = Depends(get_current_user)) -> User:
#     if current_user.role not in ["admin", "judge"]:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return current_user

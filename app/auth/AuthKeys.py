from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d24e094faa6ca2356c818166b7a9563c93f7099f6f0f4caa6cf63b98e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
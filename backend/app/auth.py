from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY,ALGORITHM
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def hash_password(password): return pwd_context.hash(password)
def verify_password(password,hashed): return pwd_context.verify(password,hashed)
def create_access_token(data,expires_minutes=30):
    payload=data.copy();payload["exp"]=datetime.now(timezone.utc)+timedelta(minutes=expires_minutes);return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
def decode_access_token(token):
    try:
        p=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]); uid=p.get("sub")
        if uid is None: raise HTTPException(status_code=401,detail="Invalid token")
        return int(uid)
    except (JWTError,ValueError): raise HTTPException(status_code=401,detail="Invalid or expired token",headers={"WWW-Authenticate":"Bearer"})
def get_current_user_id(token:str=Depends(oauth2_scheme)): return decode_access_token(token)
def get_current_user(db, user_id):
    from app.models import User
    u=db.query(User).filter(User.id==user_id).first()
    if not u: raise HTTPException(status_code=401,detail="User not found")
    return u
def require_user(db,user_id): return get_current_user(db,user_id)

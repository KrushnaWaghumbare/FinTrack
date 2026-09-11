from datetime import datetime,timedelta,timezone
import hashlib,secrets
from fastapi import APIRouter,Depends,HTTPException,Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User,PasswordResetToken
from app.schemas import UserCreate,ForgotPasswordRequest,ResetPasswordRequest
from app.auth import hash_password,verify_password,create_access_token,get_current_user_id,get_current_user
from app.config import RESET_TOKEN_MINUTES
from app.email_service import send_reset_email
router=APIRouter(prefix="/api/auth",tags=["Auth"])
@router.post("/register",status_code=201)
def register(data:UserCreate,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==data.email).first(): raise HTTPException(400,"Email already registered")
    u=User(email=data.email,password_hash=hash_password(data.password),role="user");db.add(u);db.commit();db.refresh(u);return {"message":"User registered","id":u.id,"email":u.email}
@router.post("/login")
def login(username:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==username).first()
    if not u or not verify_password(password,u.password_hash): raise HTTPException(401,"Invalid email or password",headers={"WWW-Authenticate":"Bearer"})
    return {"access_token":create_access_token({"sub":str(u.id),"role":u.role}),"token_type":"bearer"}
@router.get("/me")
def me(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    u=get_current_user(db,user_id);return {"id":u.id,"email":u.email,"role":u.role,"created_at":u.created_at}
@router.post("/forgot-password")
def forgot(data:ForgotPasswordRequest,db:Session=Depends(get_db)):
    # Constant response avoids account enumeration.
    u=db.query(User).filter(User.email==data.email).first()
    if u:
        raw=secrets.token_urlsafe(48);h=hashlib.sha256(raw.encode()).hexdigest();now=datetime.now(timezone.utc)
        db.query(PasswordResetToken).filter(PasswordResetToken.user_id==u.id,PasswordResetToken.used_at.is_(None)).update({"used_at":now},synchronize_session=False)
        db.add(PasswordResetToken(user_id=u.id,token_hash=h,expires_at=now+timedelta(minutes=RESET_TOKEN_MINUTES)));db.commit()
        try: send_reset_email(u.email,raw)
        except Exception: raise HTTPException(503,"Password reset email is temporarily unavailable. Please try again later.")
    return {"message":"If an account exists for that email, a password reset link has been sent."}
@router.post("/reset-password")
def reset(data:ResetPasswordRequest,db:Session=Depends(get_db)):
    h=hashlib.sha256(data.token.encode()).hexdigest();now=datetime.now(timezone.utc)
    r=db.query(PasswordResetToken).filter(PasswordResetToken.token_hash==h,PasswordResetToken.used_at.is_(None),PasswordResetToken.expires_at>now).first()
    if not r: raise HTTPException(400,"Invalid or expired reset link")
    u=db.query(User).filter(User.id==r.user_id).first()
    if not u: raise HTTPException(400,"Invalid reset request")
    u.password_hash=hash_password(data.password);r.used_at=now;db.commit();return {"message":"Password reset successfully"}

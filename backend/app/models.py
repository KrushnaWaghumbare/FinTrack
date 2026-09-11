from sqlalchemy import Column,Integer,String,DateTime,Numeric,ForeignKey,Boolean,Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True,nullable=False)
    password_hash=Column(String,nullable=False)
    role=Column(String,nullable=False,default="user",server_default="user")
    created_at=Column(DateTime(timezone=True),server_default=func.now())
class Transaction(Base):
    __tablename__="transactions"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    amount=Column(Numeric(12,2),nullable=False)
    type=Column(String,nullable=False)
    category=Column(String,nullable=False)
    subcategory=Column(String,nullable=True)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=True)
    subcategory_id=Column(Integer,ForeignKey("subcategories.id"),nullable=True)
    description=Column(String,nullable=True)
    transaction_date=Column(DateTime(timezone=True),server_default=func.now())
class Budget(Base):
    __tablename__="budgets"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    category=Column(String,nullable=False)
    amount=Column(Numeric(12,2),nullable=False)
    month=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,index=True,nullable=False)
    enabled=Column(Boolean,nullable=False,default=True,server_default="1")
    created_at=Column(DateTime(timezone=True),server_default=func.now())
class Subcategory(Base):
    __tablename__="subcategories"
    id=Column(Integer,primary_key=True,index=True)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False,index=True)
    name=Column(String,nullable=False)
    enabled=Column(Boolean,nullable=False,default=True,server_default="1")
    created_at=Column(DateTime(timezone=True),server_default=func.now())
class PasswordResetToken(Base):
    __tablename__="password_reset_tokens"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    token_hash=Column(String(64),unique=True,index=True,nullable=False)
    expires_at=Column(DateTime(timezone=True),nullable=False)
    used_at=Column(DateTime(timezone=True),nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

class SavingsGoal(Base):
    __tablename__='savings_goals'
    id=Column(Integer,primary_key=True,index=True); user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    name=Column(String(100),nullable=False); target_amount=Column(Numeric(12,2),nullable=False); saved_amount=Column(Numeric(12,2),nullable=False,default=0)
    target_date=Column(DateTime(timezone=True),nullable=True); created_at=Column(DateTime(timezone=True),server_default=func.now())

class Account(Base):
    __tablename__='accounts'
    id=Column(Integer,primary_key=True,index=True); user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    name=Column(String(100),nullable=False); type=Column(String(30),nullable=False,default='cash'); balance=Column(Numeric(12,2),nullable=False,default=0); currency=Column(String(8),nullable=False,default='INR'); enabled=Column(Boolean,nullable=False,default=True); created_at=Column(DateTime(timezone=True),server_default=func.now())

class RecurringTransaction(Base):
    __tablename__='recurring_transactions'
    id=Column(Integer,primary_key=True,index=True); user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    amount=Column(Numeric(12,2),nullable=False); type=Column(String(20),nullable=False); category=Column(String(80),nullable=False); subcategory=Column(String(80),nullable=True); description=Column(String,nullable=True)
    frequency=Column(String(20),nullable=False); next_date=Column(DateTime(timezone=True),nullable=False); enabled=Column(Boolean,nullable=False,default=True); created_at=Column(DateTime(timezone=True),server_default=func.now())

class UserSession(Base):
    __tablename__='user_sessions'
    id=Column(Integer,primary_key=True,index=True); user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True); token_hash=Column(String(64),unique=True,index=True,nullable=False); created_at=Column(DateTime(timezone=True),server_default=func.now()); last_seen_at=Column(DateTime(timezone=True),server_default=func.now()); revoked_at=Column(DateTime(timezone=True),nullable=True)

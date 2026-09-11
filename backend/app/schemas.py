from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel,EmailStr,Field
class UserCreate(BaseModel): email:EmailStr; password:str=Field(min_length=8,max_length=128)
class LoginForm(BaseModel): email:EmailStr; password:str
class ForgotPasswordRequest(BaseModel): email:EmailStr
class ResetPasswordRequest(BaseModel): token:str=Field(min_length=20); password:str=Field(min_length=8,max_length=128)
class TransactionCreate(BaseModel):
    amount:Decimal=Field(gt=0); type:str; category:str=Field(min_length=1,max_length=80); subcategory:str|None=Field(default=None,max_length=80); category_id:int|None=None; subcategory_id:int|None=None; description:str|None=None; transaction_date:datetime|None=None
class BudgetCreate(BaseModel): category:str=Field(min_length=1,max_length=80); amount:Decimal=Field(gt=0); month:str=Field(pattern=r"^\d{4}-\d{2}$")
class CategoryCreate(BaseModel): name:str=Field(min_length=2,max_length=80); enabled:bool=True
class SubcategoryCreate(BaseModel): category_id:int; name:str=Field(min_length=2,max_length=80); enabled:bool=True

class SavingsGoalCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100); target_amount:Decimal=Field(gt=0); saved_amount:Decimal=Field(default=0,ge=0); target_date:datetime|None=None
class AccountCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100); type:str=Field(default='cash',max_length=30); balance:Decimal=0; currency:str=Field(default='INR',max_length=8); enabled:bool=True
class RecurringCreate(BaseModel):
    amount:Decimal=Field(gt=0); type:str; category:str=Field(min_length=1,max_length=80); subcategory:str|None=None; description:str|None=None; frequency:str=Field(pattern=r'^(daily|weekly|monthly|yearly)$'); next_date:datetime; enabled:bool=True
class PasswordChange(BaseModel):
    current_password:str=Field(min_length=1); new_password:str=Field(min_length=8,max_length=128)
class ProfileUpdate(BaseModel):
    email:EmailStr

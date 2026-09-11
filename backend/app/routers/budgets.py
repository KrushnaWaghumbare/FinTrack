from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Budget,Transaction,Category
from app.schemas import BudgetCreate
from app.auth import get_current_user_id
router=APIRouter(prefix="/api/budgets",tags=["Budgets"])
@router.get("")
def get_budgets(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    return db.query(Budget).filter(Budget.user_id==user_id).order_by(Budget.month.desc(),Budget.id.desc()).all()
@router.post("",status_code=201)
def create_budget(data:BudgetCreate,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    if db.query(Budget).filter(Budget.user_id==user_id,Budget.category==data.category,Budget.month==data.month).first(): raise HTTPException(409,"Budget already exists for this category and month")
    b=Budget(user_id=user_id,category=data.category,amount=data.amount,month=data.month);db.add(b);db.commit();db.refresh(b);return b
@router.put("/{budget_id}")
def update_budget(budget_id:int,data:BudgetCreate,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    b=db.query(Budget).filter(Budget.id==budget_id,Budget.user_id==user_id).first()
    if not b: raise HTTPException(404,"Budget not found")
    b.category=data.category;b.amount=data.amount;b.month=data.month;db.commit();return b
@router.delete("/{budget_id}")
def delete_budget(budget_id:int,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    b=db.query(Budget).filter(Budget.id==budget_id,Budget.user_id==user_id).first()
    if not b: raise HTTPException(404,"Budget not found")
    db.delete(b);db.commit();return {"message":"Budget deleted"}
@router.get("/analytics")
def get_budget_analytics(month:str,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    budgets=db.query(Budget).filter(Budget.user_id==user_id,Budget.month==month).all();out=[]
    for b in budgets:
        expenses=db.query(Transaction).filter(Transaction.user_id==user_id,Transaction.type=="expense",Transaction.category==b.category).all()
        spent=sum(float(t.amount or 0) for t in expenses if t.transaction_date and t.transaction_date.strftime("%Y-%m")==month)
        budget=float(b.amount);remaining=budget-spent;pct=(spent/budget*100) if budget else 0
        out.append({"budget_id":b.id,"category":b.category,"budget":budget,"spent":spent,"remaining":remaining,"percentage":pct,"status":"Over Budget" if remaining<0 else "Within Budget"})
    return out

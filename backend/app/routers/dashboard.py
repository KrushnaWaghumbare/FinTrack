from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Transaction
from app.auth import get_current_user_id
router=APIRouter(prefix="/api/dashboard",tags=["Dashboard"])
@router.get("/summary")
def summary(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    income=float(db.query(func.coalesce(func.sum(Transaction.amount),0)).filter(Transaction.user_id==user_id,Transaction.type=="income").scalar() or 0)
    expense=float(db.query(func.coalesce(func.sum(Transaction.amount),0)).filter(Transaction.user_id==user_id,Transaction.type=="expense").scalar() or 0)
    return {"total_income":income,"total_expense":expense,"balance":income-expense}
@router.get("/categories")
def categories(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    rows=db.query(Transaction.category,func.sum(Transaction.amount)).filter(Transaction.user_id==user_id,Transaction.type=="expense").group_by(Transaction.category).all();return [{"category":r[0],"total":float(r[1])} for r in rows]
@router.get("/monthly")
def monthly(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    ts=db.query(Transaction).filter(Transaction.user_id==user_id).all();m={}
    for t in ts:
        if not t.transaction_date: continue
        k=t.transaction_date.strftime("%Y-%m");m.setdefault(k,{"month":k,"income":0,"expense":0});m[k][t.type]+=float(t.amount or 0)
    return [m[k] for k in sorted(m)]

from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func,extract
from app.database import get_db
from app.models import Transaction,Budget,SavingsGoal,Account,RecurringTransaction,User,UserSession
from app.schemas import SavingsGoalCreate,AccountCreate,RecurringCreate,PasswordChange,ProfileUpdate
from app.auth import get_current_user_id,get_current_user,verify_password,hash_password

router=APIRouter(prefix='/api',tags=['FinTrack Pro'])
def own(db,model,item_id,user_id):
    x=db.query(model).filter(model.id==item_id,model.user_id==user_id).first()
    if not x: raise HTTPException(404,'Record not found')
    return x

@router.get('/savings-goals')
def goals(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    return db.query(SavingsGoal).filter(SavingsGoal.user_id==uid).order_by(SavingsGoal.target_date.asc()).all()
@router.post('/savings-goals',status_code=201)
def goal(data:SavingsGoalCreate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    if data.saved_amount>data.target_amount: raise HTTPException(400,'Saved amount cannot exceed target')
    x=SavingsGoal(user_id=uid,**data.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.put('/savings-goals/{id}')
def goal_update(id:int,data:SavingsGoalCreate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,SavingsGoal,id,uid)
    if data.saved_amount>data.target_amount: raise HTTPException(400,'Saved amount cannot exceed target')
    for k,v in data.model_dump().items(): setattr(x,k,v)
    db.commit();db.refresh(x);return x
@router.delete('/savings-goals/{id}')
def goal_delete(id:int,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,SavingsGoal,id,uid);db.delete(x);db.commit();return {'message':'Savings goal deleted'}

@router.get('/accounts')
def accounts(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)): return db.query(Account).filter(Account.user_id==uid).order_by(Account.created_at.desc()).all()
@router.post('/accounts',status_code=201)
def account(data:AccountCreate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=Account(user_id=uid,**data.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.put('/accounts/{id}')
def account_update(id:int,data:AccountCreate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,Account,id,uid)
    for k,v in data.model_dump().items(): setattr(x,k,v)
    db.commit();db.refresh(x);return x
@router.delete('/accounts/{id}')
def account_delete(id:int,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,Account,id,uid);x.enabled=False;db.commit();return {'message':'Account disabled'}

@router.get('/recurring')
def recurring(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)): return db.query(RecurringTransaction).filter(RecurringTransaction.user_id==uid).order_by(RecurringTransaction.next_date).all()
@router.post('/recurring',status_code=201)
def recurring_create(data:RecurringCreate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    if data.type not in ('income','expense'): raise HTTPException(400,'Type must be income or expense')
    x=RecurringTransaction(user_id=uid,**data.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.put('/recurring/{id}')
def recurring_update(id:int,data:RecurringCreate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,RecurringTransaction,id,uid)
    for k,v in data.model_dump().items(): setattr(x,k,v)
    db.commit();db.refresh(x);return x
@router.delete('/recurring/{id}')
def recurring_delete(id:int,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,RecurringTransaction,id,uid);x.enabled=False;db.commit();return {'message':'Recurring transaction disabled'}
@router.post('/recurring/{id}/run')
def recurring_run(id:int,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    x=own(db,RecurringTransaction,id,uid)
    if not x.enabled: raise HTTPException(400,'Recurring transaction is disabled')
    t=Transaction(user_id=uid,amount=x.amount,type=x.type,category=x.category,subcategory=x.subcategory,description=x.description,transaction_date=x.next_date)
    db.add(t); d=x.next_date
    delta={'daily':relativedelta(days=1),'weekly':relativedelta(weeks=1),'monthly':relativedelta(months=1),'yearly':relativedelta(years=1)}[x.frequency];x.next_date=d+delta;db.commit();return {'message':'Transaction created','transaction_id':t.id,'next_date':x.next_date}

@router.get('/notifications')
def notifications(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    month=datetime.now().strftime('%Y-%m'); budgets=db.query(Budget).filter(Budget.user_id==uid,Budget.month==month).all();out=[]
    for b in budgets:
        spent=sum((float(t.amount) for t in db.query(Transaction).filter(Transaction.user_id==uid,Transaction.type=='expense',Transaction.category==b.category).all() if t.transaction_date and t.transaction_date.strftime('%Y-%m')==month), 0)
        pct=float(spent)/float(b.amount)*100 if b.amount else 0
        if pct>=100: out.append({'level':'critical','title':f'{b.category} budget exceeded','message':f'{float(spent):.2f} spent of {float(b.amount):.2f}','percentage':pct})
        elif pct>=80: out.append({'level':'warning','title':f'{b.category} budget is near limit','message':f'{pct:.0f}% of budget used','percentage':pct})
    return out

@router.get('/analytics/advanced')
def advanced(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    ts=db.query(Transaction).filter(Transaction.user_id==uid).all(); inc=sum(float(t.amount) for t in ts if t.type=='income');exp=sum(float(t.amount) for t in ts if t.type=='expense')
    cats={}
    for t in ts:
        if t.type=='expense': cats[t.category]=cats.get(t.category,0)+float(t.amount)
    months={}
    for t in ts:
        m=t.transaction_date.strftime('%Y-%m') if t.transaction_date else 'unknown'; months.setdefault(m,{'income':0,'expense':0});months[m][t.type]+=float(t.amount)
    return {'income':inc,'expense':exp,'savings':inc-exp,'savings_rate':(inc-exp)/inc*100 if inc else 0,'top_categories':sorted([{'category':k,'amount':v} for k,v in cats.items()],key=lambda x:x['amount'],reverse=True)[:10],'monthly':sorted([{'month':k,**v} for k,v in months.items()],key=lambda x:x['month'])}

@router.get('/calendar')
def calendar(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    ts=db.query(Transaction).filter(Transaction.user_id==uid).all();rec=db.query(RecurringTransaction).filter(RecurringTransaction.user_id==uid,RecurringTransaction.enabled==True).all()
    return {'transactions':[{'id':t.id,'date':t.transaction_date,'title':t.description or t.category,'amount':t.amount,'type':t.type} for t in ts], 'recurring':[{'id':r.id,'date':r.next_date,'title':r.description or r.category,'amount':r.amount,'type':r.type} for r in rec]}

@router.put('/profile')
def profile(data:ProfileUpdate,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    u=get_current_user(db,uid)
    existing=db.query(User).filter(User.email==data.email,User.id!=uid).first()
    if existing: raise HTTPException(409,'Email is already in use')
    u.email=data.email;db.commit();return {'id':u.id,'email':u.email,'role':u.role}
@router.post('/security/change-password')
def change_password(data:PasswordChange,uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    u=get_current_user(db,uid)
    if not verify_password(data.current_password,u.password_hash): raise HTTPException(400,'Current password is incorrect')
    u.password_hash=hash_password(data.new_password);db.commit();return {'message':'Password changed successfully'}
@router.get('/security/sessions')
def sessions(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)): return db.query(UserSession).filter(UserSession.user_id==uid,UserSession.revoked_at.is_(None)).order_by(UserSession.last_seen_at.desc()).all()
@router.post('/security/revoke-all')
def revoke_all(uid:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    db.query(UserSession).filter(UserSession.user_id==uid,UserSession.revoked_at.is_(None)).update({'revoked_at':datetime.now(timezone.utc)},synchronize_session=False);db.commit();return {'message':'All other sessions revoked'}

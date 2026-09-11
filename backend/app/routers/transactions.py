from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction,Category,Subcategory
from app.schemas import TransactionCreate
from app.auth import get_current_user_id
router=APIRouter(prefix="/api/transactions",tags=["Transactions"])
def validate_taxonomy(data,db):
    # Custom values are intentionally allowed when the user chooses "Other"
    # (or supplies a custom name). IDs are only attached to predefined taxonomy.
    data.category = data.category.strip()
    if not data.category:
        raise HTTPException(400,"Category cannot be empty")
    if data.subcategory is not None:
        data.subcategory = data.subcategory.strip() or None

    if data.category_id:
        c=db.query(Category).filter(Category.id==data.category_id,Category.enabled==True).first()
        if not c: raise HTTPException(400,"Category is disabled or invalid")
        data.category=c.name
    else:
        # A category without an ID is a valid custom category. If it matches an
        # enabled predefined category, attach its ID automatically.
        c=db.query(Category).filter(Category.name.ilike(data.category),Category.enabled==True).first()
        if c:
            data.category=c.name; data.category_id=c.id

    if data.subcategory_id:
        s=db.query(Subcategory).filter(Subcategory.id==data.subcategory_id,Subcategory.enabled==True).first()
        if not s or (data.category_id and s.category_id!=data.category_id):
            raise HTTPException(400,"Invalid subcategory for selected category")
        data.subcategory=s.name; data.subcategory_id=s.id
    elif data.subcategory:
        # Predefined subcategories get their relationship/ID. A non-matching
        # value is preserved as a custom subcategory instead of being rejected.
        if data.category_id:
            s=db.query(Subcategory).filter(Subcategory.category_id==data.category_id,Subcategory.name.ilike(data.subcategory),Subcategory.enabled==True).first()
            if s:
                data.subcategory=s.name; data.subcategory_id=s.id
        # No category ID means this is a custom category + custom subcategory.
    return data
@router.post("/",status_code=201)
def create_transaction(data:TransactionCreate,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    if data.type not in ["income","expense"]: raise HTTPException(400,"Type must be income or expense")
    validate_taxonomy(data,db);t=Transaction(user_id=user_id,amount=data.amount,type=data.type,category=data.category,subcategory=data.subcategory,category_id=data.category_id,subcategory_id=data.subcategory_id,description=data.description,transaction_date=data.transaction_date)
    db.add(t);db.commit();db.refresh(t);return {"message":"Transaction created successfully","transaction_id":t.id,"amount":t.amount,"type":t.type,"category":t.category,"subcategory":t.subcategory}
@router.get("/")
def get_transactions(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    ts=db.query(Transaction).filter(Transaction.user_id==user_id).order_by(Transaction.transaction_date.desc()).all()
    return [{"id":t.id,"user_id":t.user_id,"amount":t.amount,"type":t.type,"category":t.category,"subcategory":t.subcategory,"category_id":t.category_id,"subcategory_id":t.subcategory_id,"description":t.description,"transaction_date":t.transaction_date} for t in ts]
@router.put("/{transaction_id}")
def update_transaction(transaction_id:int,data:TransactionCreate,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    t=db.query(Transaction).filter(Transaction.id==transaction_id,Transaction.user_id==user_id).first()
    if not t: raise HTTPException(404,"Transaction not found")
    if data.type not in ["income","expense"]: raise HTTPException(400,"Type must be income or expense")
    validate_taxonomy(data,db);t.amount=data.amount;t.type=data.type;t.category=data.category;t.subcategory=data.subcategory;t.category_id=data.category_id;t.subcategory_id=data.subcategory_id;t.description=data.description
    if data.transaction_date: t.transaction_date=data.transaction_date
    db.commit();return {"message":"Transaction updated successfully","transaction_id":t.id}
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id:int,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    t=db.query(Transaction).filter(Transaction.id==transaction_id,Transaction.user_id==user_id).first()
    if not t: raise HTTPException(404,"Transaction not found")
    db.delete(t);db.commit();return {"message":"Transaction deleted successfully","transaction_id":transaction_id}

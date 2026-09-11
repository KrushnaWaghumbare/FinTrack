from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category,Subcategory,Transaction
from app.schemas import CategoryCreate,SubcategoryCreate
from app.auth import get_current_user_id,get_current_user
router=APIRouter(prefix="/api/categories",tags=["Categories"])
def admin(db,uid):
    u=get_current_user(db,uid)
    if u.role!="admin": raise HTTPException(403,"Admin permission required")
    return u
def tree(db,include_disabled=False):
    cats=db.query(Category).order_by(Category.name).all();out=[]
    for c in cats:
        if not include_disabled and not c.enabled: continue
        subs=db.query(Subcategory).filter(Subcategory.category_id==c.id).order_by(Subcategory.name).all()
        if not include_disabled: subs=[s for s in subs if s.enabled]
        out.append({"id":c.id,"name":c.name,"enabled":c.enabled,"subcategories":[{"id":s.id,"category_id":s.category_id,"name":s.name,"enabled":s.enabled} for s in subs]})
    return out
@router.get("")
def get_categories(include_disabled:bool=False,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    if include_disabled: admin(db,uid)
    return tree(db,include_disabled)
@router.post("",status_code=201)
def create(data:CategoryCreate,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    admin(db,uid)
    if db.query(Category).filter(Category.name.ilike(data.name)).first(): raise HTTPException(409,"Category already exists")
    c=Category(name=data.name.strip(),enabled=data.enabled);db.add(c);db.commit();db.refresh(c);return {"id":c.id,"name":c.name,"enabled":c.enabled}
@router.post("/subcategories",status_code=201)
def create_sub(data:SubcategoryCreate,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    admin(db,uid);c=db.query(Category).filter(Category.id==data.category_id).first()
    if not c: raise HTTPException(404,"Category not found")
    if db.query(Subcategory).filter(Subcategory.category_id==c.id,Subcategory.name.ilike(data.name)).first(): raise HTTPException(409,"Subcategory already exists")
    s=Subcategory(category_id=c.id,name=data.name.strip(),enabled=data.enabled);db.add(s);db.commit();db.refresh(s);return {"id":s.id,"category_id":s.category_id,"name":s.name,"enabled":s.enabled}
@router.put("/subcategories/{subcategory_id}")
def update_sub(subcategory_id:int,data:SubcategoryCreate,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    admin(db,uid);s=db.query(Subcategory).filter(Subcategory.id==subcategory_id).first();c=db.query(Category).filter(Category.id==data.category_id).first()
    if not s or not c: raise HTTPException(404,"Subcategory or category not found")
    dup=db.query(Subcategory).filter(Subcategory.id!=subcategory_id,Subcategory.category_id==c.id,Subcategory.name.ilike(data.name)).first()
    if dup: raise HTTPException(409,"Subcategory already exists")
    s.category_id=c.id;s.name=data.name.strip();s.enabled=data.enabled;db.commit();return {"id":s.id,"category_id":s.category_id,"name":s.name,"enabled":s.enabled}
@router.delete("/subcategories/{subcategory_id}")
def delete_sub(subcategory_id:int,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    admin(db,uid);s=db.query(Subcategory).filter(Subcategory.id==subcategory_id).first()
    if not s: raise HTTPException(404,"Subcategory not found")
    s.enabled=False;db.commit();return {"message":"Subcategory disabled; existing relationships preserved"}
@router.put("/{category_id}")
def update(category_id:int,data:CategoryCreate,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    admin(db,uid);c=db.query(Category).filter(Category.id==category_id).first()
    if not c: raise HTTPException(404,"Category not found")
    dup=db.query(Category).filter(Category.id!=category_id,Category.name.ilike(data.name)).first()
    if dup: raise HTTPException(409,"Category already exists")
    c.name=data.name.strip();c.enabled=data.enabled;db.commit();return {"id":c.id,"name":c.name,"enabled":c.enabled}
@router.delete("/{category_id}")
def delete(category_id:int,db:Session=Depends(get_db),uid:int=Depends(get_current_user_id)):
    admin(db,uid);c=db.query(Category).filter(Category.id==category_id).first()
    if not c: raise HTTPException(404,"Category not found")
    c.enabled=False
    db.query(Subcategory).filter(Subcategory.category_id==c.id).update({"enabled":False},synchronize_session=False)
    db.commit();return {"message":"Category disabled; existing relationships preserved"}

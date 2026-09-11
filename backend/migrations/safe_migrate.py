from sqlalchemy import inspect,text
from app.database import engine
from app.models import Base,Category,Subcategory
from app.database import SessionLocal

def add_column(table,column,definition):
    cols={c["name"] for c in inspect(engine).get_columns(table)}
    if column not in cols:
        with engine.begin() as c: c.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}"))

def run():
    # Create new tables first; existing tables are never dropped.
    Base.metadata.create_all(bind=engine)
    if "users" in inspect(engine).get_table_names():
        add_column("users","role","VARCHAR(20) DEFAULT 'user'")
    if "transactions" in inspect(engine).get_table_names():
        add_column("transactions","subcategory","VARCHAR")
        add_column("transactions","category_id","INTEGER")
        add_column("transactions","subcategory_id","INTEGER")
    db=SessionLocal()
    try:
        if db.query(Category).count()==0:
            seeds={"Home":["Rent","Electricity","Water","Internet","Maintenance"],"Food":["Groceries","Dining","Coffee"],"Transport":["Fuel","Public transport","Taxi"],"Shopping":["Clothing","Electronics","Household"],"Healthcare":["Doctor","Medicine"],"Entertainment":["Movies","Games","Subscriptions"],"Salary":[],"Other":[]}
            for name,subs in seeds.items():
                c=Category(name=name,enabled=True);db.add(c);db.flush()
                for s in subs: db.add(Subcategory(category_id=c.id,name=s,enabled=True))
            db.commit()
    finally: db.close()
if __name__=="__main__": run()

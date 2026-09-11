from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base,engine
from app import models
from app.routers import auth,transactions,budgets,dashboard,categories,features
from migrations.safe_migrate import run as migrate
migrate()
app=FastAPI(title="Personal Finance API",version="2.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router);app.include_router(transactions.router);app.include_router(budgets.router);app.include_router(dashboard.router);app.include_router(categories.router);app.include_router(features.router)
@app.get("/")
def root(): return {"message":"Personal Finance API is running!"}
@app.get("/db-test")
def db_test():
    with engine.connect() as c: return {"database":c.exec_driver_sql("SELECT 1").scalar()}

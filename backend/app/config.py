import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./finance.db")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","HS256")
if not SECRET_KEY: raise RuntimeError("SECRET_KEY is required in .env")
SMTP_HOST=os.getenv("SMTP_HOST")
SMTP_PORT=int(os.getenv("SMTP_PORT","587"))
SMTP_USER=os.getenv("SMTP_USER")
SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
SMTP_FROM=os.getenv("SMTP_FROM",SMTP_USER or "")
FRONTEND_URL=os.getenv("FRONTEND_URL","http://localhost:5173")
RESET_TOKEN_MINUTES=int(os.getenv("RESET_TOKEN_MINUTES","30"))

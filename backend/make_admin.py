import os
from app.database import SessionLocal
from app.models import User
email=os.getenv('ADMIN_EMAIL')
if not email:
    raise SystemExit('Set ADMIN_EMAIL first, e.g. PowerShell: $env:ADMIN_EMAIL="you@example.com"')
db=SessionLocal()
try:
    u=db.query(User).filter(User.email==email).first()
    if not u: raise SystemExit(f'User not found: {email}')
    u.role='admin';db.commit();print(f'Admin enabled for {email}')
finally: db.close()

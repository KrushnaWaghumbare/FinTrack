# FinTrack — Feature Update Setup

This backend is designed to sit on the existing database. It does not drop tables or delete historical transactions during category management.

### 1. Replace backend app files
Copy the `backend/app` folder and `backend/migrations` folder into the existing backend. Keep your existing `.env` values; add the SMTP values shown below.

### 2. Install backend dependencies
`pip install -r requirements.txt`

### 3. Configure email reset
Add to `.env`:
```
FRONTEND_URL=http://localhost:5173
RESET_TOKEN_MINUTES=30
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-gmail@example.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM=your-gmail@example.com
```
Use an SMTP app password, not your normal mailbox password.

### 4. Run migration/API
From `backend`:
`uvicorn app.main:app --reload`
The startup migration only creates missing tables and adds nullable columns; existing records are preserved.

### 5. Enable an existing admin
Do not allow public registration to select `admin`. In PowerShell:
```
$env:ADMIN_EMAIL="your-existing-account@example.com"
python make_admin.py
```
Then sign out/in so the frontend receives the admin role.

### 6. Frontend
Copy the updated frontend files into your existing frontend. Run:
```
npm install
npm run dev
```
New frontend dependencies are `xlsx` and `jspdf`.

### Features
- Forgot password: hashed, single-use, expiring reset tokens + SMTP email.
- CSV/Excel/PDF: exports the currently filtered/displayed transaction rows.
- Dynamic category/subcategory database tree with admin CRUD and enable/disable.
- Category rename keeps the same ID; disable is used instead of physical deletion.
- Transaction category/subcategory selection is dependent and database-backed.
- Existing legacy transactions retain their original text values.

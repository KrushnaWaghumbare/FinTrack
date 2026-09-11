import smtplib
from email.message import EmailMessage
from app.config import SMTP_HOST,SMTP_PORT,SMTP_USER,SMTP_PASSWORD,SMTP_FROM,FRONTEND_URL

def send_reset_email(to_email,token):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD and SMTP_FROM):
        raise RuntimeError("SMTP is not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD and SMTP_FROM.")
    url=f"{FRONTEND_URL.rstrip('/')}/reset-password?token={token}"
    msg=EmailMessage();msg["Subject"]="FinTrack password reset";msg["From"]=SMTP_FROM;msg["To"]=to_email
    msg.set_content(f"We received a password reset request for your FinTrack account.\n\nReset your password: {url}\n\nThis link expires automatically and can be used only once. If you did not request this, you can ignore this email.")
    with smtplib.SMTP(SMTP_HOST,SMTP_PORT,timeout=15) as s:
        s.starttls();s.login(SMTP_USER,SMTP_PASSWORD);s.send_message(msg)

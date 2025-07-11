import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import ssl
load_dotenv()

msg = EmailMessage()




ticker = yf.Ticker("GC=F")

history = ticker.history(period='2d')

history.reset_index(inplace=True)
last_closing_price = history['Close'].iloc[-1].round(2)
timestamp = history['Date'].iloc[-1]
date = f"{timestamp.year}-{timestamp.month}-{timestamp.day}"

email_content = f"The closing price for gold for the corresponding date {date} is {last_closing_price:2f} $"
msg.set_content(email_content)
msg['From'] = os.environ.get("MSG_FROM")
email_pass = os.environ.get("EMAIL_PASS")
msg['To'] = os.environ.get("MSG_TO")
msg["Subject"] = f'Gold price Update'


context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login("testanddev101@gmail.com",email_pass)
    smtp.sendmail(os.environ.get("MSG_FROM"),os.environ.get("MSG_TO"),msg.as_string())
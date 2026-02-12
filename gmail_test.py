import smtplib

EMAIL = "payalmohapatra137@gmail.com"
PASSWORD = "dlmjdwnwrpmcrbqh"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    print("✅ Login successful!")
    server.quit()
except Exception as e:
    print("❌ Login failed:")
    print(e)

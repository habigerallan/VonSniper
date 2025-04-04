from email.message import EmailMessage
from html.parser import HTMLParser
import requests
import smtplib

BASE_URL = "https://www.vonmaur.com/Results.aspx?sale=y&md=c&cat=650&pg=1"
BRANDS = {
    "COACH": 2168,
    "BDG": 190209
}

DISCOUNT_THRESHOLD = 70

notified_products = set()
emails_to_notify = set()
brands_to_check = set()

def create_url():
    pass

def get_html(url):
    pass

def get_items(html):
    pass

def calculate_discount(item):
    pass

def create_email(item):
    pass

def notify_emails():
    pass

def main():
    pass
    
        
if __name__ == "__main__":
    main()
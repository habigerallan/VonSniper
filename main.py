from email.message import EmailMessage
import requests
import smtplib
import time
from bs4 import BeautifulSoup
import os

BASE_URL = "https://www.vonmaur.com/Results.aspx?sale=y&md=c&cat=650&pg=1"
BRANDS = {
    "COACH": 2168,
    "BDG": 190209
}
DISCOUNT_THRESHOLD = 70

notified_products = set()
brands_to_check = {"COACH","BDG"}

def create_url(brand_id):
    return f"{BASE_URL}&br={brand_id}&fsf=br"

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1'
    }

    cookies = {
        '__RequestVerificationToken': os.getenv('REQUEST_VERIFICATION_TOKEN'),
        'ASP.NET_SessionId': os.getenv('ASP_SESSION_ID'),
        'PIM-SESSION-ID': os.getenv('PIM_SESSION_ID'),
        'bm_sz': os.getenv('BM_SZ'),
        'bm_mi': os.getenv('BM_MI'),
        '_abck': os.getenv('ABCK'),
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    return response.text

def get_items(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    product_containers = soup.find_all("div", class_="divResultsProduct")

    for container in product_containers:
        try:
            url = "https://www.vonmaur.com" + container.find("a")["href"]

            title = container.find("a", {"aria-label": True}).text.strip()

            brand = container.find("div", class_="divBrandName").text.strip()

            old_price_text = container.find("div", class_="spnOrigPrice")
            new_price_text = container.find("div", class_="spnCurrPrice")

            old_price = float(old_price_text.text.replace("$", "").strip()) if old_price_text else None
            new_price = float(new_price_text.text.replace("$", "").strip()) if new_price_text else None

            items.append({
                "title": title,
                "brand": brand,
                "old_price": old_price,
                "new_price": new_price,
                "url": url
            })
        except:
            print(f"Error parsing product: {url}")
            continue

    return items

def calculate_discount(item):
    old_price = item["old_price"]
    new_price = item["new_price"]
    return round((old_price - new_price) / old_price * 100)

def start_listening():
    for brand, brand_id in BRANDS.items():
        if brand not in brands_to_check:
            continue
        url = create_url(brand_id)
        html = get_html(url)
        items = get_items(html)
        for item in items:
            discount = calculate_discount(item)
            if discount >= DISCOUNT_THRESHOLD and item["url"] not in notified_products:
                print(item["url"])
                notified_products.add(item["url"])

def main():
    while True:
        print("Checking for new deals...")
        start_listening()
        time.sleep(600)

if __name__ == "__main__":
    main()

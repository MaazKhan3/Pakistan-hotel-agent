import requests

CITY = "Islamabad"
URL = f"https://www.booking.com/searchresults.html?ss={CITY}&ssne={CITY}&ssne_untouched={CITY}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

response = requests.get(URL, headers=HEADERS)

with open("booking_islamabad_sample.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"Saved HTML to booking_islamabad_sample.html. Status code: {response.status_code}") 
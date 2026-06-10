import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

print("Script started...")

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

def get_star_rating(rating_word):
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return ratings.get(rating_word, 0)

print("Sending request to website...")

try:
    response = requests.get(START_URL, timeout=10)
    print(f"Status Code: {response.status_code}")
except Exception as e:
    print(f"ERROR: {e}")
    exit()

all_books = []
url = START_URL
page = 1

while url and page <= 10:
    print(f"Scraping Page {page}...")

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    print(f"  Found {len(books)} books on this page")

    for book in books:
        title = book.find("h3").find("a")["title"]
        price = book.find("p", class_="price_color").text.strip()
        price_clean = float(price.replace("Â£", "").replace("£", "").replace("\xa3", ""))
        rating_tag = book.find("p", class_="star-rating")
        rating_word = rating_tag["class"][1]
        star_rating = get_star_rating(rating_word)
        availability = book.find("p", class_="instock availability").text.strip()
        book_url = BASE_URL + book.find("h3").find("a")["href"].replace("../", "")

        all_books.append({
            "Title": title,
            "Price (£)": price_clean,
            "Star Rating": star_rating,
            "Availability": availability,
            "Book URL": book_url
        })

    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_page = next_btn.find("a")["href"]
        url = BASE_URL + next_page
        page += 1
        time.sleep(1)
    else:
        url = None

df = pd.DataFrame(all_books)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv("books_dataset.csv", index=False)

print(f"\n✅ Done! Total Books: {len(df)}")
print(f"💾 Saved to books_dataset.csv")
print(f"\nPreview:")
print(df.head(5).to_string(index=False))
print(f"\nStats:")
print(f"  Avg Price: £{df['Price (£)'].mean():.2f}")
print(f"  5-Star Books: {len(df[df['Star Rating'] == 5])}")
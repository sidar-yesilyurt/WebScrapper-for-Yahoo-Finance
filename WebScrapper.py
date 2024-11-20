import requests
from bs4 import BeautifulSoup

def get_positive_crypto(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")  # Find the main table containing crypto data
        
        rows = table.find_all("tr")[1:]  # To skip the header row
        positive_coins = []  # List to store positive coins
        
        # Iterate through rows, extract coin name and change percentage
        for row in rows[:25]: # Only go till row 25
            cols = row.find_all("td")
            if len(cols) >= 5:  # Ensure row has enough columns
                coin_name = cols[0].text.strip()
                change = cols[4].text.strip()
                
                # Check if change contains '+' sign for only getting positive changes
                try:
                    if "+" in change:
                        positive_coins.append((coin_name, change))
                except ValueError:
                    continue
        
        return positive_coins
    else:
        print(f"Error: Couldn't fetch page {response.status_code}")
        return []

def process_multiple_pages(base_url, max_pages=5):

    # Processes multiple pages of cryptocurrency data from the given base URL.
    # Initialize variables to keep track of page numbers and starting position
    page_start = 0 
    page_count = 1   
    
    # Continue scraping pages until max_pages
    while page_count <= max_pages:
        # Construct the URL for the current page
        url = f"{base_url}?start={page_start}&count=25"
        print(f"Scraping page {page_count}...")
        
        # Fetch positive cryptocurrency changes for this page and assign it
        page_data = get_positive_crypto(url)
        
        # Process the data for this page
        if page_data:
            print(f"Page {page_count}: All positive coins")
            # Print each coin name and its change percentage
            for i, (name, change) in enumerate(page_data, 1):
                print(f"{i}. {name}: {change}")
        else:
            print(f"Page {page_count}: No positive coins found")
        
        # Move to the next page by incrementing the starting position
        page_start += 25
        # Increment the page count
        page_count += 1


# Run the scraper
process_multiple_pages("https://finance.yahoo.com/markets/crypto/all/")

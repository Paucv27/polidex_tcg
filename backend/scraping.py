from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from utils import meanPrice, getStats
from playwright.sync_api import sync_playwright
#cheerio equivalent for python = package for web scraping that turns info to json instead of html ?


def inputCardInfo():
    """
    Get user input in terminal for card name, promo and number
    These are stored as global variables
    """
    
    global cardName, cardNumber
    
    cardName = input("Input card name: ")

    cardNumber = input("Input card number: ")


def formatCardInfo(name,number):
    """
    Formats card info replacing spaces with '+' so they can be used in the search

    Args:
        name (str): Name of the card (e.g. Politoed EX)
        number (str): Number of the card in the set

    Returns:
        str: Formatted string
    """
    
    return f"{(name+"+"+number).replace(' ','+')}"


def fetchListings(cardName,cardNumber):
    """
    Scrapes ebay search for top 5 matches of the specified card (in order of most recently sold)

    Args:
        cardName (str): Card Name
        cardNumber (str): Card Number in Set

    Returns:
        List[dict]: Fetched listings in dict format
    """

    SIMILARITY_THRESHOLD=65

    #setUrlAndHeaders(cardName,cardNumber)
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw=pokemon+tcg+{cardName}+{cardNumber}&LH_Complete=1&LH_Sold=1".replace(" ","")
    
    print("Searching for: ",url)
    
    # scrapes the whole html page specified in the url (containing the formatted card info)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)  
        # headless=True means no window pops up
        page = browser.new_page()

        # helps avoid bot detection
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept-Language": "en-GB,en;q=0.9"
        })

        page.goto(url)

        # waits until at least one listing appears instead of the captcha page
        page.wait_for_selector("li.s-card", timeout=10000)

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")
        
        print(page.url)
            
        if "splashui/challenge" in page.url:
            print("BLOCKED BY CAPTCHA")
            return
        
        print("finding listings")
        # had to dig in the html code for this smh my head
        # should make this broader but right now this works for testing
        listings = soup.find_all("li", class_="s-card s-card--horizontal s-card--dark-solt-links-blue s-card--overflow")
        
        cards=[]
        
        print("running loop...")

        for listing in listings: 
            
            # same issue here, these classes are too specific and change frequently so I need a broader solution
            title_span = listing.find("span", class_="su-styled-text primary default")
            title = title_span.text.strip() if title_span else "N/A"
            print("Title: ", title)

            price_span = listing.find("span", class_="su-styled-text positive bold large-1 s-card__price")
            price = price_span.text.strip() if price_span else "£0.00"
            print("Price: ", price)

            link_a = listing.find("a", class_="su-link")
            link = link_a["href"] if link_a else "N/A"
            print("Link: ", link)

            sold_date_span = listing.find("span", class_="su-styled-text positive default")
            sold_date = sold_date_span.text.strip() if sold_date_span else "N/A"
            print("Date Sold: ", sold_date)
            
            # only if they exist
            if title and price and link and not "to" in price:
                
                print("COMPARING :",cardName+" "+cardNumber,"\nCOMPARING:", title)
                
                # only append to resulting list if this comparison returns a similarity score of 70 or more
                # without this I would get results for other cards, such as a Houndoom (not searching for this)
                # or I would not include cards that have 1 wrong letter in the name, such as Houndoor (searching for this)
                similarityScore = round(fuzz.partial_ratio(cardName.lower()+' '+cardNumber, title.lower()),2)
                print("Score: ",similarityScore)
                
                if similarityScore >= SIMILARITY_THRESHOLD:
                    
                    print("MATCH WITH ",similarityScore,"%\nADDED TO RETURN LIST"+"! - "*50)
                
                    cards.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "date_sold": sold_date if sold_date else "Unknown",
                        "similarity": similarityScore
                    })
                    
                # so only the first 5 matching listings are stored (for now)
                if len(cards) >= 5:
                    break
                
            print("\n======================================\n")
                
        cards = sorted(cards, key=lambda x: float(x["price"].replace("£","")), reverse=True)
        
        printFormatted(cards)
        
        getStats(cards) # gotta send this to front-end too

        browser.close()
        
        return cards


def printFormatted(cards):
    
    print("\n................. CARDS FETCHED ..................\n")
    
    for card in cards:
        
        print(f"Name: {card["title"]}\nPrice: {card["price"]}\nLink: {card["link"]}\nDate Sold: {card["date_sold"]}\nSimilarity: {card["similarity"]}")
        print("\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")
    
    
#for testing
if __name__=="__main__":
    
    fetchedCards=fetchListings("Leafeon EX", "006/131")
    
    getStats(fetchedCards)
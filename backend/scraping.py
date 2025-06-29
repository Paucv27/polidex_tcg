import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from utils import meanPrice, getStats
#cheerio equivalent for python = package for web scraping that turns info to json instead of html

def setUrlAndHeaders(cardName,cardNumber):
    """
    Sets search URL using card name and number, and sets headers to spoof a visit

    Args:
        name (str): Name of the card (e.g. Politoed EX)
        number (str): Number of the card in the set

    Returns:
        Nothing
    """
    
    global url, headers

    url = f'https://www.ebay.co.uk/sch/i.html?_nkw=pokemon+tcg+{formatCardInfo(cardName,cardNumber)}&LH_Complete=1&LH_Sold=1'

    # so ebay doesnt block my requests as this is a program and not me, this mimics "me"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
               "Accept-Language": "en-GB,en;q=0.9",
               "Referer": "https://www.google.com/",}


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


def fetchListings(name,number):

    SIMILARITY_THRESHOLD=70

    setUrlAndHeaders(name,number)
    
    print("Searching for: ",url)
    
    # scrapes the whole html page specified in the url (containing the formatted card info)
    # headers dict is used to spoof a visit to the page
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        
        print("running parser")
        
        # parses the html to a BeautifulSoup object, which represents the document as a nested data structure
        soup = BeautifulSoup(response.text, "html.parser")
        
        # had to dig in the html code for this smh my head
        listings = soup.find_all("li", class_="s-item s-item__dsa-on-bottom s-item__pl-on-bottom")
        
        cards=[]
        
        for listing in listings:
            
            title = listing.select_one(".s-item__title").text
            print("Title: ", title)
            price = listing.select_one(".s-item__price").text
            print("Price: ", price)
            link = listing.find("a", class_="s-item__link")["href"]
            print("Link: ", link)
            sold_date = listing.select_one(".s-item__caption").text
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
        
        return cards
    else:
        print(f"Request failed with status code {response.status_code}")


def printFormatted(cards):
    
    print("\n................. CARDS FETCHED ..................\n")
    
    for card in cards:
        
        print(f"Name: {card["title"]}\nPrice: {card["price"]}\nLink: {card["link"]}\nDate Sold: {card["date_sold"]}\nSimilarity: {card["similarity"]}")
        print("\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")
    
    
#for testing
if __name__=="__main__":
    
    fetchedCards=fetchListings()
    
    getStats(fetchedCards)
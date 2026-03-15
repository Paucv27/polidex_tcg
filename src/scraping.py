import time

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from utils import meanPrice, getStats
#cheerio equivalent for python = package for web scraping that turns info to json instead of html

SIMILARITY_THRESHOLD=70

def setUrlAndHeaders():
    
    global url, headers

    # maybe switch to ebay API
    url = f'https://www.ebay.co.uk/sch/i.html?_nkw=pokemon+tcg+{formatCardInfo(cardName,cardNumber)}&LH_Complete=1&LH_Sold=1'

    # so ebay doesnt block my requests as this is a program and not me, this mimics "me"
    # temp
    ua = UserAgent()
    
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }


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


def fetchListings():
    
    inputCardInfo()
    setUrlAndHeaders()
    formatCardInfo(cardName,cardNumber)
    
    print("Searching for: ",url)
    
    # headers dict is used to spoof a visit to the page
    session = requests.Session()
    session.headers.update(headers)    
    
    try:        
        # get cookies
        session.get("https://www.ebay.co.uk", timeout=10)
        
        # scrapes the whole html page specified in the url (containing the formatted card info)
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            
            print("running parser...")
            
            # parses the html to a BeautifulSoup object, which represents the document as a nested data structure
            soup = BeautifulSoup(response.text, "html.parser")
            
            # had to dig in the html code for this smh my head
            # keeps changing
            print(soup)
            with open("soup.txt", "w", encoding="utf-8") as file:
                file.write(soup.prettify())
                file.close()
                
            # right now we are getting blocked by a bot checker probs
            listings = soup.find_all("li", class_="s-card s-card--horizontal s-card--overflow")
            if not listings:
                print("\nProbably blocked by Bot checker :(\ncheck soup.txt for actual HTML structure")
                return []
            
            cards=[]
            
            for listing in listings:
                
                # these also keep changing
                title = listing.select_one(".s-card__title").text
                print("Title: ", title)
                price = listing.select_one(".s-card__price").text
                print("Price: ", price)
                link = listing.find("a", class_="s-card__link")["href"]
                print("Link: ", link)
                sold_date = listing.select_one(".s-card__caption").text
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
                        
                        print("MATCH WITH ",similarityScore,"%\nADDED TO RETURN LIST "+"#"*50)
                    
                        cards.append({
                            "title": title,
                            "price": float(price.replace(",","").replace("£","")),
                            "link": link,
                            "date_sold": sold_date if sold_date else "Unknown",
                            "similarity": similarityScore
                        })
                        
                    # so only the first 5 matching listings are stored (for now)
                    if len(cards) >= 5:
                        break
                    
                print("\n======================================\n")
                    
            # this might need a fix
            cards = sorted(cards, key=lambda x: x["price"], reverse=True)
            
            printFormatted(cards)
            
            return cards
        else:
            # error msg
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
        


def printFormatted(cards):
    
    print("\n................. CARDS FETCHED ..................\n")
    
    for card in cards:
        
        print(f"Name: {card["title"]}\nPrice: {card["price"]}\nLink: {card["link"]}\nDate Sold: {card["date_sold"]}\nSimilarity: {card["similarity"]}")
        print("\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")
    
    
#for testing
if __name__=="__main__":
    
    fetchedCards=fetchListings()
    
    getStats(fetchedCards)
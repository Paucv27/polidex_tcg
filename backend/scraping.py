import logging
import time
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from utils import getStats
#cheerio equivalent for python = package for web scraping that turns info to json instead of html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD=70

def fetchListings(cardName, cardNumber):
    
    url, headers = setUrlAndHeaders(cardName, cardNumber)

    logger.info("Searching for: %s", url)

    # headers dict is used to spoof a visit to the page
    session = requests.Session()
    session.headers.update(headers)    
    
    try:        
        # quick request to ebay to get cookies, otherwise the main request could be blocked
        session.get("https://www.ebay.co.uk", timeout=10)
        # scrapes the whole html page specified in the url (containing the formatted card info)
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            logger.info("Running parser...")
            
            # parses the html to a BeautifulSoup object, which represents the document as a nested data structure
            soup = BeautifulSoup(response.text, "html.parser")
            with open("soup.txt", "w", encoding="utf-8") as file:
                logger.info("Writing soup to soup.txt...")
                file.write(soup.prettify())
                file.close()
                
            # ERRORS:
            # 1. Sometimes scraper gets blocked by bot checker
            # 2. classname keeps changing, so need to search the html structure for the actual class name
            listings = soup.find_all("li", class_="s-card s-card--horizontal s-card--pagination-below s-card--overflow s-card--overflow__bottom s-card--su-overflow")
            if not listings:
                logger.error("Probably blocked by Bot checker :( -> check soup.txt for actual HTML structure or wait a bit before retrying")
                return []
            
            cards=[]
            for listing in listings:
                
                # these also keep changing
                title = listing.select_one(".s-card__title").text
                price = listing.select_one(".s-card__price").text
                link = listing.find("a", class_="s-card__link")["href"]
                sold_date = listing.select_one(".s-card__caption").text
                
                logger.info("Card: %s", title)
                logger.debug("Info: %s | %s | %s", price, link, sold_date)
                
                # only if they exist
                if title and price and link and not "to" in price:
                    # only append to resulting list if this comparison returns a similarity score of 70 or more
                    # without this I would get results for other cards, such as a Houndoom (not searching for this)
                    # or I would not include cards that have 1 wrong letter in the name, such as Houndoor (searching for this)
                    similarityScore = round(fuzz.partial_ratio(cardName.lower()+' '+cardNumber, title.lower()),2)
                    logger.debug("Similarity Score (2dp): %s", similarityScore)

                    if similarityScore >= SIMILARITY_THRESHOLD:
                        logger.info("^^^^^^^^^ card added to return list ^^^^^^^^^\n")
                    
                        cards.append({
                            "title": title,
                            "price": float(price.replace(",","").replace("£","")), # only accepts gbp for now, otherwise will throw an error
                            "link": link,
                            "date_sold": sold_date if sold_date else "Unknown",
                            "similarity": similarityScore,
                            "cardName": cardName,
                            "cardNumber": cardNumber
                        })
                        
                    # so only the first 5 matching listings are stored (for now)
                    if len(cards) >= 5:
                        break
                    
            # this might need a fix
            cards = sorted(cards, key=lambda x: x["price"], reverse=True)
            printFormatted(cards)
            
            return cards
        else:
            # error msg
            logger.error(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return []
    

def setUrlAndHeaders(cardName, cardNumber):

    # maybe switch to ebay API
    url = f'https://www.ebay.co.uk/sch/i.html?_nkw=pokemon+tcg+{(cardName+"+"+cardNumber).replace(' ','+')}&LH_Complete=1&LH_Sold=1'

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
    
    return url, headers
    

def printFormatted(cards):
    logger.info("Printing formatted cards...")
    
    print("\n................. CARDS FETCHED ..................\n")
    for card in cards:
        print(f"Name: {card['title']}\nPrice: {card['price']}\nLink: {card['link']}\nDate Sold: {card['date_sold']}\nSimilarity: {card['similarity']}")
        print("\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")
    
    
#for testing
if __name__=="__main__":
    
    fetchedCards=fetchListings("Leafeon EX", "006/131")
    
    getStats(fetchedCards)
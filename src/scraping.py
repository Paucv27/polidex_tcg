import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

SIMILARITY_THRESHOLD=70

def setUrlAndHeaders():
    
    global url, headers

    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={formatCardInfo(cardName,cardPromo,cardNumber)}&LH_Complete=1&LH_Sold=1"

    # so ebay doesnt block my requests as this is a program and not me, this mimics "me"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
               "Accept-Language": "en-GB,en;q=0.9",
               "Referer": "https://www.google.com/",}


def inputCardInfo():
    """
    Get user input in terminal for card name, promo and number
    These are stored as global variables
    """
    
    global cardName, cardPromo, cardNumber
    
    cardName = input("Input card name: ")

    cardPromo = input("Input card promo: ")

    cardNumber = input("Input card number: ")


def formatCardInfo(name,promo,number):
    """
    Formats card info replacing spaces with '+' so they can be used in the search

    Args:
        name (str): Name of the card (e.g. Politoed EX)
        promo (str): Promo the card belongs to (set)
        number (str): Number of the card in the set

    Returns:
        str: Formatted string
    """
    
    return f"{(name+promo+number).replace(' ','+')}"


def fetchListings():
    
    inputCardInfo()
    setUrlAndHeaders()
    formatCardInfo(cardName,cardPromo,cardNumber)
    
    print("Searching for: ",url)
    
    # scrapes the whole html page specified in the url (containing the formatted card info)
    # headers dict is used to spoof a visit to the page
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        
        # parses the html to a BeautifulSoup object, which represents the document as a nested data structure
        soup = BeautifulSoup(response.text, "html.parser")
        
        # had to dig in the html code for this smh my head
        listings = soup.find_all("li", class_="s-item s-item__pl-on-bottom")
        
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
            if title and price and link:
                
                print("COMPARING :",cardName,"\nCOMPARING:", title)
                
                # only append to resulting list if this comparison returns a similarity score of 70 or more
                # without this I would get results for other cards, such as a Houndoom (not searching for this)
                # or I would not include cards that have 1 wrong letter in the name, such as Houndoor (searching for this)
                similarityScore = round(fuzz.partial_ratio(cardName.lower(), title.lower()),2)
                if similarityScore >= SIMILARITY_THRESHOLD:
                    
                    print("MATCH WITH ",similarityScore,"%\nADDED TO RETURN LIST")
                
                    cards.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "date_sold": sold_date if sold_date else "Unknown",
                        "similarity": similarityScore
                    })
                    
                print("\n======================================\n")
                    
                # so only the first 5 matching listings are stored (for now)
                if len(cards) >= 5:
                    break
        
        printFormatted(cards)
        return cards
    else:
        
        # error msg
        print(f"Request failed with status code {response.status_code}")


def printFormatted(cards):
    
    for card in cards:
        
        print(f"Name: {card["title"]}\nPrice: {card["price"]}\nLink: {card["link"]}\nDate Sold: {card["date_sold"]}\nSimilarity: {card["similarity"]}")
        print("\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

fetchListings()
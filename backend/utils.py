# could include any helper functions used by any other modules

# if there are too many or different types, I could modularise into a utils folder and have individual helpers inside

import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getStats(cards: list):
    
    if not cards or len(cards) == 0:
        logger.warning("No listings to analyze :(")
        return
    
    total = getPriceTotal(cards)
    avg = getPriceAvg(cards)
    range = getPriceRange(cards)
    
    logger.info("Total is %s (2dp) from %d listings", round(total, 2), len(cards))
    logger.info("Mean price: %s | Rounded (2dp): %s", avg, round(avg, 2))
    logger.info("Ranges from %s", range)


def getPriceTotal(listings:list) -> float:   
    
    return sum(listing["price"] for listing in listings)   
    
    
def getPriceRange(listings:list) -> str:
    
    return f"{min(listing['price'] for listing in listings)} - {max(listing['price'] for listing in listings)}"
        
    
def getPriceAvg(listings:list) -> float:
    
    total = getPriceTotal(listings)   
    avg = 0 if len(listings) == 0 else total/len(listings)          
        
    return avg
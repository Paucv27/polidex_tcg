# could include any helper functions used by any other modules

# if there are too many or different types, I could modularise into a utils folder and have individual helpers inside

import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getStats(cards: list) -> tuple[float, float, float, float]:
    """
    Returns the total, average and range of prices from a list of card listings.
    
    Args:
        cards (list): A list of card listings, which are dictionaries with card information including price.
    
    Returns:
        tuple[float, float, float, float]: A tuple containing the total, average, min, and max prices (in that order).
        
    """
    
    if not cards or len(cards) == 0:
        logger.warning("No listings to analyze :(")
        raise ValueError("Cannot calculate stats: empty card list")
    
    total = getPriceTotal(cards)
    avg = getPriceAvg(cards)
    min, max = getPriceRange(cards)
    
    logger.debug("Total is %s (2dp) from %d listings", round(total, 2), len(cards))
    logger.debug("Mean price: %s | Rounded (2dp): %s", avg, round(avg, 2))
    logger.debug("Ranges from %s", f"{min} - {max}")
    
    return total, avg, min, max


def getPriceTotal(listings:list) -> float:   
    
    return sum(listing["price"] for listing in listings)   
    
    
def getPriceRange(listings:list) -> tuple[float, float]:
    
    return min(listing['price'] for listing in listings), max(listing['price'] for listing in listings)
        
    
def getPriceAvg(listings:list) -> float:
    
    total = getPriceTotal(listings)   
    avg = 0 if len(listings) == 0 else total/len(listings)          
        
    return avg
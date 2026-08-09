# could include any helper functions used by any other modules

# if there are too many or different types, I could modularise into a utils folder and have individual helpers inside

def getStats(cards):
    
    if not cards:
        return
    
    print("$-$-$-$ Statistics about the fetched listings $-$-$-$\n")
    
    print("MEAN"+"-"*50+"\n")
    mean=meanPrice(cards)
    print("Mean price: ",mean," || Rounded: ",round(mean,2),"\n")
    
    print("RANGE"+"-"*50+"\n")
    range=rangePrice(cards)
    print("Ranges from ",range)
    
    
def rangePrice(listings:list) -> str:
    
    min = 1000000
    max = 0
    
    for listing in listings:
        
        x = listing["price"]
        
        if x<min:
            min = x
            
        if x>max:
            max = x
            
    print(min," - ",max)
    
    return f"{min} - {max}"
        
    
def meanPrice(listings:list) -> float:
    
    total = 0
    
    for listing in listings:
        
        total += listing["price"]
        
    print(f"Total is {total} (2dp) from {len(listings)} listings")
    
    mean = 0
    
    try:
        mean = total/len(listings)
    except:
        print("Error calculating mean - returning 0")
            
        
    return mean
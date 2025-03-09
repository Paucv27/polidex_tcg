# could include any helper functions used by any other modules

# if there are too many or different types, I could modularise into a utils folder and have individual helpers inside

def mean(listings:list) -> float:
    
    print("Getting mean prices...")
    
    mean = 0
    
    for listing in listings:
        
        mean+=listings["price"] 
        
    return mean     
    
# Polidex - TCG Card Recognition

_No live website as of yet, but will be coming soon!_

Polidex is a proof-of-concept app made for fun, simply to test my own skills in making an app similar to TCGplayer. It works by running an image recognition pipeline to extract text from card images, then passes the name and card number to the web scraping script. This will scrape ebay for matching, sold listings, and collect data for simple price analysis.

As per, emojis/ASCII art from https://emojicombos.com/ !



## Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/paucv27/polidex_tcg.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Start backend and frontend
    ```bash
    cd backend
    flask run
        
    cd frontend
    npm run dev
    ```

Once front-end and back-end are running, check localhost for front-end to use the web app!

- Test data (cards) can be found in the project folder (./data/...). I haven't tried using actual photos of cards yet (and the current algorithm is "fine-tuned" for this perfect dataset), so use these for now while I work on that :p at the end of the day, its a demo


## Files and directories
- `backend/app.py`: Simple backend Flask app with a single route for running the processing pipeline.
- `backend/recognition.py`: Code for recognizing Pokémon cards using image processing with CV2 and EasyOCR.
- `backend/scraping.py`: Code for web scraping eBay for card prices. Prone to errors caused by eBay classnames frequently changing. Needs frequent manual updating.
- `backend/utils.py`: Helper functions that are frequently reused and can be used for insights.
- `data/`: Contains two sets of Pokémon cards used for testing the functionality of the app. Some cards will be easier to recognise than others because of the noise created by their background art.
- `frontend/`: Contains all front-end code in Javascript and CSS (React Framework).

## Legal Disclaimer

### Pokémon IP Notice
Pokémon and all related characters, images, and trademarks are property of **The Pokémon Company, Nintendo, Game Freak, Creatures, and/or Wizards of the Coast**. 

This application is an independent, fan-made tool for card identification and is **not produced by, endorsed by, supported by, or affiliated with** any of these companies.

### Data Sources
- All card price data is sourced from publicly available eBay listings
- Prices are provided for informational purposes only
- This tool does not guarantee accuracy of pricing or availability

### Usage
- For entertainment purposes only
- Not for commercial use
- User-uploaded images are not stored or saved

### License
This project is for educational and personal use only.

# Polidex - TCG Card Recognition

_No live website as of yet, but will be coming soon!_

Polidex is a proof-of-concept app made for fun, simply to test my own skills in making an app similar to TCGplayer. It works by running an image recognition pipeline to extract text from card images, then passes the name and card number to the web scraping script. This will scrape ebay for matching, sold listings, and collect data for simple price analysis.

As per, emojis/ASCII art from https://emojicombos.com/ !

## Architecture & Technologies

- **Frontend:** React.js, Tailwind CSS
- **Backend:** Flask (Python REST API)
- **Computer Vision:** OpenCV (Image processing & thresholding), EasyOCR (Metadata extraction)
- **Data Engineering:** BeautifulSoup4 (Web scraping), Pandas (Data normalization)

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/paucv27/polidex_tcg.git
   cd polidex_tcg
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
### Running the application

1. **Start the Flask Backend:**
   ```bash
   cd backend
   flask run
   ```
2. **Start the React Frontend:**
   ```bash
   cd frontend
   npm install && npm run dev
   ```
   
Access the web application interface via `http://localhost:XXXX` (your local Vite/React port).

- Test data (cards) can be found in the project folder (./data/...). I haven't tried using actual photos of cards yet (and the current algorithm is "fine-tuned" for this perfect dataset), so use these for now while I work on that :p at the end of the day, its a demo

## Files and directories
- `backend/app.py`: Simple backend Flask app with a single route for running the processing pipeline.
- `backend/recognition.py`: Code for recognizing Pokémon cards using image processing with CV2 and EasyOCR.
- `backend/scraping.py`: Code for web scraping eBay for card prices. Prone to errors caused by eBay classnames frequently changing. Needs frequent manual updating.
- `backend/utils.py`: Helper functions that are frequently reused and can be used for insights.
- `data/`: Contains two sets of Pokémon cards used for testing the functionality of the app. Some cards will be easier to recognise than others because of the noise created by their background art.
- `frontend/`: Contains all front-end code in Javascript and CSS (React Framework).

## Legal Disclaimer
- **IP Notice:** Pokémon and all associated assets are trademarks of The Pokémon Company, Nintendo, Game Freak, and Creatures. This is an independent, non-commercial educational research project.
- **Data Usage:** Price metrics are fetched from public listings for informational purposes only. No user data or images are stored or persisted.

### License
This project is for educational and personal use only.

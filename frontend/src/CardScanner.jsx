import React, { useState } from 'react';
import './CardScanner.css';

const CardScanner = () => {
    const [preview, setPreview] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [cards, setCards] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [noCards, setNoCards] = useState(false);
    const [insights, setInsights] = useState(null);
    const [detectedCard, setDetectedCard] = useState(null);

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {

            const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                setError('Please upload a valid image file (JPEG, PNG, WebP, or GIF)');
                return;
            }

            if (file.size > 5 * 1024 * 1024) {
                setError('Image size must be less than 5MB');
                return;
            }

            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setCards(null);
            setError(null);
            setInsights(null);
            setDetectedCard(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedFile) {
            setError('Please select a card image first!');
            return;
        }

        setIsLoading(true);
        setError(null);
        setCards(null);
        setNoCards(false);

        const formData = new FormData();
        formData.append('image', selectedFile);

        console.log('Submitted card to Polidex - Awaiting response...');

        try {
            const response = await fetch('http://localhost:5000/process-image', {
                method: 'POST',
                body: formData,
            });

            const text = await response.text();
            console.log('Raw response text:', text);

            try {
                const result = JSON.parse(text);
                console.log('Parsed JSON:', result);

                if(result.error) {
                    setError(result.error);
                    setNoCards(false);
                    setCards(null);
                    setInsights(null);
                    setDetectedCard(result.detected);
                } else if (result.cards && result.cards.length > 0) {
                    setCards(result.cards);
                    setInsights(result.stats);
                    setDetectedCard(result.detected);
                    setNoCards(false);
                } else {
                    setCards(null);
                    setInsights(null);
                    setDetectedCard(null);
                    setNoCards(true);
                }
            } catch (parseError) {
                console.error('Failed to parse JSON:', parseError);
                setError('Failed to parse server response. Please try again.');
            }
        } catch (fetchError) {
            console.error('Network error:', fetchError);
            setError('Failed to connect to server. Please ensure the backend is running.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            <div className="scanner-container">
                <div className="upload-section">
                    <div className="card-header">
                        <h1 className="title" style={{ color: '#1e7727' }}>
                            Polidex TCG Scanner
                        </h1>
                        <p className="subtitle">Get insights about your Pokémon cards !</p>
                        <p style={{ fontSize: '24px' }}>🀥 🀣 🀦 🀧 🀨</p>
                    </div>
                    
                    <form onSubmit={handleSubmit} className="upload-form">
                        <div className="image-preview-container">
                            {preview ? (
                                <div className="image-preview">
                                    <img src={preview} alt="Card preview" />
                                    <button 
                                        className="remove-image"
                                        onClick={() => {
                                            setPreview(null);
                                            setSelectedFile(null);
                                            setCards(null);
                                        }}
                                    >
                                        ✕
                                    </button>
                                </div>
                            ) : (
                                <div className="placeholder">
                                    <div className="placeholder-icon">◓</div>
                                    <p>CARD PREVIEW</p>
                                    <span className="placeholder-sub">Upload an image to begin !</span>
                                </div>
                            )}
                        </div>

                        <div className="button-group">
                            <label className="btn btn-upload">
                                <span>🗁 Choose Image</span>
                                <input 
                                    type="file" 
                                    accept="image/*" 
                                    capture="environment" 
                                    onChange={handleImageChange}
                                    disabled={isLoading}
                                />
                            </label>

                            <button 
                                type="submit" 
                                className={`btn btn-scan ${!selectedFile || isLoading ? 'disabled' : ''}`}
                                disabled={!selectedFile || isLoading}
                            >
                                {isLoading ? (
                                    <>
                                        <span className="spinner"></span>
                                        Scanning...
                                    </>
                                ) : (
                                    '⛶ Scan Card'
                                )}
                            </button>
                        </div>
                    </form>
                </div>

                <div className="results-section">
                    {isLoading && (
                        <div className="loading-state">
                            <div className="loading-spinner"></div>
                            <p>Analyzing card...</p>
                            <span className="loading-sub">Checking listings</span>
                        </div>
                    )}

                    {!isLoading && (error || noCards) && (
                        <div className="no-results-state">
                            <div className="no-results-icon">⚠</div>
                            <h3>Oops! Something unexpected happened...</h3>
                            <p>
                                Sometimes the scanner doesn't correctly detect the cards, 
                                or the scraper gets blocked by eBay, sorry! 
                                Maybe try again with a different card?
                            </p>
                            <p style={{ color: '#00290787', fontSize: '10px' }}>Error: {error}</p>
                            <p style={{ color: '#005a3687', fontSize: '10px' }}>Detected Card: {detectedCard?.name || 'Unknown'} #{detectedCard?.number || '???'}</p>
                            <button 
                                className="btn btn-retry"
                                onClick={() => {
                                    setError(null);
                                    setNoCards(false);
                                    setSelectedFile(null);
                                    setPreview(null);
                                    setCards(null);
                                    setInsights(null);
                                    setDetectedCard(null);
                                }}
                            >
                                Try Again
                            </button>
                        </div>
                    )}

                    {cards && cards.length > 0 && (
                        <div className="results-content">
                            <div className="results-header">
                                <h2>
                                    <span className="results-icon">◓</span>
                                    Found {cards.length} Listings - Sorted by Price (Highest to Lowest)
                                </h2>
                                <span className="results-badge">eBay</span>
                            </div>
                            <p style={{ fontSize: '10px', color: '#364b3b89', textAlign: 'center' }}>
                                Results may be inaccurate if the detected card name or number is not similar enough to the intended card.
                            </p>

                            {(insights) && (
                            <div className="insights-section">
                                <div className="insights-grid">
                                    <div className="insight-card">
                                        <span className="insight-label">Detected Card</span>
                                        <span className="insight-value">
                                            {detectedCard?.name || 'Unknown'} #{detectedCard?.number || '???'}
                                        </span>
                                    </div>
                                    <div className="insight-card">
                                        <span className="insight-label">Sum of Card Prices</span>
                                        <span className="insight-value">£{insights.total?.toFixed(2) || '0.00'}</span>
                                    </div>
                                    <div className="insight-card">
                                        <span className="insight-label">Average Card Price</span>
                                        <span className="insight-value">£{insights.avg?.toFixed(2) || '0.00'}</span>
                                    </div>
                                    <div className="insight-card">
                                        <span className="insight-label">Card Price Range</span>
                                        <span className="insight-value">
                                            £{insights.min?.toFixed(2) || '0.00'} - £{insights.max?.toFixed(2) || '0.00'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            )}

                            <div className="listings-list">
                                {cards.map((listing, index) => (
                                    <div key={index} className="listing-card">
                                        <div className="listing-rank">
                                            #{index + 1}
                                        </div>
                                        <div className="listing-content">
                                            <div className="listing-header">
                                                <h3 className="listing-title">
                                                    {listing.title || 'Unknown Card'}
                                                </h3>
                                                <div className="listing-similarity">
                                                    <div className="similarity-bar">
                                                        <div 
                                                            className="similarity-fill"
                                                            style={{ width: `${listing.similarity}%` }}
                                                        ></div>
                                                    </div>
                                                    <span className="similarity-text">
                                                        {listing.similarity}% match
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="listing-details">
                                                <div className="listing-price">
                                                    <span className="price-label">Price</span>
                                                    <span className="price-value">
                                                        £{listing.price.toFixed(2)}
                                                    </span>
                                                </div>
                                                <div className="listing-date">
                                                    <span className="date-label">Sold</span>
                                                    <span className="date-value">
                                                        {listing.date_sold || 'Unknown date'}
                                                    </span>
                                                </div>
                                            </div>
                                            <a 
                                                href={listing.link} 
                                                target="_blank" 
                                                rel="noopener noreferrer"
                                                className="listing-link"
                                                color="#29738e"
                                            >
                                                View Listing &gt;&gt;
                                            </a>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {!isLoading && !cards && !error && !noCards &&(
                        <div className="empty-state">
                            <div className="empty-dot-art">
                                <pre style={{
                                    fontFamily: 'monospace',
                                    whiteSpace: 'pre',
                                    lineHeight: '1.2',
                                    fontSize: '8px',
                                    color: '#29738e',
                                    margin: 0,
                                    padding: 0,
                                    userSelect: 'none',
                                    pointerEvents: 'none',
                                    opacity: 0.6
                                }}>
{`⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⣶⣿⣶⣦⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⣶⣾⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⠿⠿⣿⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡀⣄⠀⠀⠀⠀⠀⠀⠀⣿⣿⠟⠉⠀⢀⣀⠀⠀⠈⠉⠀⠀⣀⣀⠀⠀⠙⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣶⣿⣿⣿⣾⣇⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠹⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⣼⡏⠀⠀⠀⣀⣀⣉⠉⠩⠭⠭⠭⠥⠤⢀⣀⣀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣿⠷⠒⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠒⠼⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢹⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣶⣤⣄⣠⣤⣤⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
⠀⠀⣀⠀⢸⡿⠿⣿⡿⠋⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠻⠿⠟⠉⢙⣿⣿⣿⣿⣿⣿⡇
⠀⠀⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀  ⠈⠻⠿⢿⡿⣿⠳⠀
⠀⠀⡞⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⢀⣇⡀⠀⠀
⢀⣸⣀⡀⠀⠀⠀⠀⣠⣴⣾⣿⣷⣆⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣰⣿⣿⣿⣿⣷⣦⠀⠀⠀⠀⢿⣿⠿⠃⠀
⠘⢿⡿⠃⠀⠀⠀⣸⣿⣿⣿⣿⣿⡿⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢻⣿⣿⣿⣿⣿⣿⠂⠀⠀⠀⡸⠁⠀⠀⠀
⠀⠀⠳⣄⠀⠀⠀⠹⣿⣿⣿⡿⠛⣠⠾⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠳⣄⠙⠛⠿⠿⠛⠉⠀⠀⣀⠜⠁⠀⠀⠀⠀
⠀⠀⠀⠈⠑⠢⠤⠤⠬⠭⠥⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠉⠒⠢⠤⠤⠤⠒⠊⠁⠀⠀⠀⠀⠀⠀`}
                                </pre>
                            </div>
                            <h3>No results yet...</h3>
                            <p>Upload a card image to see matching eBay listings</p>
                        </div>
                    )}
                    <div className="footer-disclaimer">
                        <div className="disclaimer-content">
                            <p className="disclaimer-main">
                                <strong>⚖ Legal Disclaimer ⚖</strong><br />
                                Pokémon and all related characters, images, and trademarks are property of 
                                <strong> The Pokémon Company, Nintendo, Game Freak, Creatures, and/or Wizards of the Coast</strong>. 
                                This application is an independent, fan-made tool for card identification and is 
                                <strong> not produced by, endorsed by, supported by, or affiliated with</strong> any of these companies.
                            </p>
                            <p className="disclaimer-sub">
                                All price data is sourced from publicly available eBay listings and is provided for informational purposes only. 
                                This tool does not guarantee accuracy of pricing or availability.
                            </p>
                            <p className="disclaimer-small">
                                For entertainment purposes only. Not for commercial use. 
                                <span className="disclaimer-separator">•</span> 
                                Images are not stored or saved.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CardScanner;
# Computer Auction Website

A website for auctioning computers.

![techprowl2](https://user-images.githubusercontent.com/47819009/128790287-2839db50-b595-4f68-a7c2-9ccd8752d4bf.png)


## Technologies Used
- HTML
- CSS
- Bootstrap
- Python
- Flask
  - Flask Templates
  - Flask WTForms
  - Flask SQLAlchemy
  - Flask Login

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd computer-auction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

The database (`auction/auction.sqlite`) is included with seed data.

## Features

### User Authentication
- User registration with email validation
- Secure login/logout
- Session management

### Listings
- Create new auction listings with title, description, starting price, and images
- View all active listings on the homepage
- View listing details including bid history
- See listing status (Active/Closed)

### Bidding
- Place bids on active listings
- Bid must be higher than current highest bid
- View bid history for each listing
- Automatic auction closure based on end date

### Watchlist
- Add/remove listings from personal watchlist
- View all watched items in one place

### Additional
- Search listings by keyword
- Post reviews on listings
- Responsive design for mobile and desktop
- Custom error pages (404, 500)
- Form validation

## Project Structure

```
computer-auction/
├── auction/
│   ├── __init__.py          # Flask app factory
│   ├── auth.py              # Authentication routes
│   ├── forms.py             # WTForms definitions
│   ├── listings.py          # Listing/bid/watchlist logic
│   ├── models.py            # Database models
│   ├── views.py             # Main routes
│   ├── auction.sqlite      # SQLite database
│   ├── static/              # CSS, images
│   └── templates/           # Jinja2 templates
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md
```

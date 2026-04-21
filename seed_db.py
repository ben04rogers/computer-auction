#!/usr/bin/env python3
"""
Seed the database with sample data.
"""

import sys

sys.path.insert(0, ".")

from auction import create_app, db
from auction.models import User, Listing, Bid, WatchListItem
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

# Sample data
laptops = [
    (
        'MacBook Pro 16" M3',
        "Apple",
        "M3",
        "18GB",
        "512GB",
        "Excellent",
        2499,
        "Powerful laptop with M3 chip, perfect for professionals.",
    ),
    (
        'MacBook Air 15" M2',
        "Apple",
        "M2",
        "16GB",
        "256GB",
        "Good",
        1499,
        "Sleek and lightweight, great for everyday use.",
    ),
    (
        "Dell XPS 15",
        "Dell",
        "i9",
        "32GB",
        "1TB",
        "Excellent",
        1899,
        "Premium Windows laptop with stunning display.",
    ),
    (
        "Dell XPS 13",
        "Dell",
        "i7",
        "16GB",
        "512GB",
        "Used",
        999,
        "Compact and powerful, slightly used.",
    ),
    (
        "HP Spectre x360",
        "HP",
        "i7",
        "16GB",
        "512GB",
        "Excellent",
        1299,
        "2-in-1 convertible with touchscreen.",
    ),
    (
        "HP EliteBook 840",
        "HP",
        "i5",
        "16GB",
        "256GB",
        "Good",
        799,
        "Business laptop, reliable and durable.",
    ),
    (
        "Lenovo ThinkPad X1",
        "Lenovo",
        "i7",
        "16GB",
        "512GB",
        "Excellent",
        1499,
        "Classic business laptop with excellent keyboard.",
    ),
    (
        "Lenovo Yoga 9i",
        "Lenovo",
        "i7",
        "16GB",
        "1TB",
        "New",
        1799,
        "Premium 2-in-1 with OLED display.",
    ),
    (
        "Microsoft Surface Laptop 5",
        "Microsoft",
        "i7",
        "16GB",
        "512GB",
        "Excellent",
        1599,
        "Elegant design with PixelSense touchscreen.",
    ),
    (
        "Surface Pro 9",
        "Microsoft",
        "i5",
        "8GB",
        "256GB",
        "Good",
        999,
        "Versatile tablet that replaces your laptop.",
    ),
    (
        "Acer Swift 5",
        "Acer",
        "i7",
        "16GB",
        "512GB",
        "Excellent",
        1199,
        "Ultra-lightweight with抗菌 coating.",
    ),
    (
        "Acer Aspire 5",
        "Acer",
        "i5",
        "8GB",
        "512GB",
        "Used",
        549,
        "Budget-friendly everyday laptop.",
    ),
]

conditions = ["New", "Excellent", "Good", "Used", "Minor defects"]

# Laptop images - use existing images
image_urls = [
    "/static/img/macbookpro13.jpg",  # MacBook Pro 16" M3
    "/static/img/macbookair11.png",  # MacBook Air 15" M2
    "/static/img/dellxps.png",  # Dell XPS 15
    "/static/img/dellxps13.jpeg",  # Dell XPS 13
    "/static/img/e410ma-bv003ts-asus-14-inch-laptop-blue-b.jpg",  # HP Spectre x360
    "/static/img/delllatitude.png",  # HP EliteBook 840
    "/static/img/thinkpad.png",  # Lenovo ThinkPad X1
    "/static/img/thinkpadx230.jpg",  # Lenovo Yoga 9i
    "/static/img/surfacelaptop2.png",  # Surface Laptop 5
    "/static/img/Surface_Pro_4.jpeg",  # Surface Pro 9
    "/static/img/test.jpg",  # Acer Swift 5
    "/static/img/152137-laptops-review-apple-macbook-pro-2020-review-image1-pbzm4ejvvs.jpg",  # Acer Aspire 5
]


def seed_database():
    app = create_app()

    with app.app_context():
        print("Seeding database...")

        # Get or create test user
        user = User.query.filter_by(name="testuser").first()
        if not user:
            user = User(
                name="testuser",
                email_id="test@example.com",
                contact_num="1234567890",
                address="123 Test St",
                password_hash=generate_password_hash("password"),
            )
            db.session.add(user)
            db.session.commit()
            print("Created user: testuser / password")

        # Clear ALL existing listings, bids, and watchlist first
        Bid.query.delete()
        WatchListItem.query.delete()
        Listing.query.delete()
        db.session.commit()

        # Create listings with unique images
        for i, (title, brand, cpu, ram, storage, condition, price, desc) in enumerate(
            laptops
        ):
            days_until_end = random.randint(1, 14)
            end_date = datetime.now() + timedelta(days=days_until_end)

            # Randomly set some as closed
            status = "Closed" if i % 4 == 0 else "Active"
            if status == "Closed":
                end_date = datetime.now() - timedelta(days=random.randint(1, 30))

            listing = Listing(
                title=title,
                starting_bid=price,
                current_bid=price + random.randint(0, 500),
                total_bids=random.randint(0, 15)
                if status == "Active"
                else random.randint(5, 20),
                brand=brand,
                cpu=cpu,
                ram_gb=ram,
                storage_gb=storage,
                condition=condition,
                end_date=end_date,
                status=status,
                description=desc,
                image_url=image_urls[i],
                seller="testuser",
            )
            db.session.add(listing)

        db.session.commit()

        # Get another user for bidding
        bidder = User.query.filter_by(name="bidder1").first()
        if not bidder:
            bidder = User(
                name="bidder1",
                email_id="bidder@example.com",
                contact_num="9876543210",
                address="456 Bidder Ave",
                password_hash=generate_password_hash("password"),
            )
            db.session.add(bidder)
            db.session.commit()

        # Add some bids to first few active listings
        active_listings = (
            Listing.query.filter_by(seller="testuser", status="Active").limit(5).all()
        )

        for listing in active_listings:
            # Add 2-5 bids per listing
            for j in range(random.randint(2, 5)):
                bid = Bid(
                    bid_amount=listing.starting_bid + (j * 100),
                    bidder_name="bidder1",
                    listing_id=listing.id,
                    bid_status="Winning" if j == random.randint(0, 4) else "Outbid",
                    bid_date=datetime.now() - timedelta(hours=random.randint(1, 48)),
                )
                db.session.add(bid)

            # Update current bid
            listing.current_bid = listing.starting_bid + random.randint(100, 400)
            listing.total_bids = random.randint(2, 5)

        db.session.commit()

        # Add some watchlist items
        WatchListItem.query.filter_by(user_id=user.id).delete()

        listings = Listing.query.filter_by(status="Active").limit(6).all()
        for listing in listings:
            watchlist_item = WatchListItem(
                user_id=user.id,
                listing_id=listing.id,
                date_added=datetime.now() - timedelta(days=random.randint(1, 7)),
            )
            db.session.add(watchlist_item)

        db.session.commit()

        total = Listing.query.count()
        active = Listing.query.filter_by(status="Active").count()
        closed = Listing.query.filter_by(status="Closed").count()

        print(f"\nDatabase seeded!")
        print(f"  Total listings: {total}")
        print(f"  Active: {active}")
        print(f"  Closed: {closed}")
        print(f"  Watchlist items: {WatchListItem.query.count()}")


if __name__ == "__main__":
    seed_database()

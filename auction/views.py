from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from .models import Listing, WatchListItem
from sqlalchemy import or_

# Create main blueprint
mainbp = Blueprint("main", __name__)


@mainbp.route("/")
def index():
    listings = Listing.query.filter_by(status="Active").all()
    watchlist_ids = []
    if current_user.is_authenticated:
        watchlist_items = WatchListItem.query.filter_by(user_id=current_user.id).all()
        watchlist_ids = [item.listing_id for item in watchlist_items]
    return render_template("index.html", listings=listings, watchlist_ids=watchlist_ids)


@mainbp.route("/search")
def search():
    # get the search string from request
    if request.args["search"]:
        item = "%" + request.args["search"] + "%"
        # use filter and like function to search for matching item
        listing = Listing.query.filter(
            or_(
                Listing.title.like(item),
                Listing.cpu.like(item),
                Listing.brand.like(item),
                Listing.ram_gb.like(item),
                Listing.storage_gb.like(item),
            ),
            Listing.status == "Active",
        )
        # Search result message
        resultMessage = "{0} results matching '{1}'".format(
            listing.count(), request.args["search"]
        )
        return render_template(
            "index.html", listings=listing, search_result=resultMessage
        )
    else:
        return redirect(url_for("main.index"))

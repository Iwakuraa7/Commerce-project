from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment


def index(request):
    active_listings = Listing.objects.exclude(active=False)

    return render(request, "auctions/index.html", {
        "listings": active_listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create_listing(request):
    # to list the categories
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = request.POST["start-bid"]
        image_url = request.POST["image-url"]
        category = Category.objects.get(pk=request.POST["category"])
        user = request.user

        # Create new listing + the user info
        new_listing = Listing(title=title, description=description, start_bid=start_bid, image_url=image_url, category=category, user=user)
        new_listing.save()

        # Create new bid with for the new listing
        new_bid = Bid(listing=new_listing, bid=start_bid)
        new_bid.save()
        # Append the new bid to the bids list of the new listing
        new_listing.bids.add(new_bid)

        return HttpResponseRedirect(reverse("create"))

    return render(request, "auctions/create-listing.html", {
            "categories": categories,
        })

@login_required(login_url="login")
def listing_page(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_user = User.objects.get(username=request.user.username)
    # Returns the max bid within the bids of the listing with the current id
    highest_bid = listing.bids.aggregate(Max('bid'))['bid__max'] or listing.start_bid
    msg = ""

    if request.method == "POST":
        new_comment = request.POST.get("new_comment")
        close_listing = request.POST.get("close_listing")
        new_bid = request.POST.get("new_bid")
        watchlist = request.POST.get("watchlist")
        remove_from_watchlist = request.POST.get("remove_from_watchlist")

        if new_comment:
            comment = Comment(listing=listing, comment=request.POST["new_comment"], user=request.user)
            comment.save()
            listing.comments.add(comment)
            msg = "Your comment has been added."

        if close_listing:
            listing.active = False
            listing.save()

            return render(request, "auctions/listing-page.html", {
            "listing": listing
            })

        if new_bid:
            new_bid = int(new_bid)
            if new_bid > listing.start_bid:
                # For this listing, append new bid, cuz its > than prev
                higher_bid = Bid(listing=listing, bid=new_bid)
                higher_bid.save()
                highest_bid = new_bid
                # Some sussy code in order to represent the highest bid on index page
                listing.start_bid = highest_bid
                # Save the current bidder user info to the listing with the current id
                listing.highest_bidder = request.user
                listing.save()
                msg = "Bid placed successfully!"
            else:
                msg = "Can't place a bid that is lower than the previous bids."

        if watchlist:
            current_user.watchlist.add(Listing.objects.get(pk=listing_id))
            msg = "Listing has been added to your watchlist."

        if remove_from_watchlist:
            current_user.watchlist.remove(Listing.objects.get(pk=listing_id))
            msg = "Listing has been removed from your watchlist"

    return render(request, "auctions/listing-page.html", {
        "listing": listing,
        "msg": msg,
        "highest_bid": highest_bid,
        "comments": listing.comments.all(),
        "is_in_watchlist": listing in current_user.watchlist.all(),
    })

@login_required(login_url="login")
def category_view(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category_choice = request.POST["category_choice"]
        related_category_pages = Listing.objects.filter(category=category_choice, active=True)
        return render(request, "auctions/categories-page.html", {
            "related_categories": related_category_pages,
            "categories": categories
        })

    return render(request, "auctions/categories-page.html", {
        "categories": categories,
    })

@login_required(login_url="login")
def watchlist_view(request):
    current_user = User.objects.get(username=request.user.username)

    return render(request, "auctions/watchlist.html", {
        "listings": current_user.watchlist.all()
    })
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid


def index(request):
    active_listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": active_listings
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
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = request.POST["start-bid"]
        image_url = request.POST["image-url"]
        category = Category.objects.get(pk=request.POST["category"])

        new_listing = Listing(title=title, description=description, start_bid=start_bid, image_url=image_url, category=category)
        new_listing.save()
        return HttpResponseRedirect(reverse("create"))

    return render(request, "auctions/create-listing.html", {
            "categories": categories,
        })

@login_required(login_url="login")
def listing_page(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # TODO: Listing page(new bid, watchlist, user_info, delete/add watchlist)
    if request.method == "POST":
        new_bid = int(request.POST["new_bid"])
        if new_bid > listing.start_bid:
            higher_bid = Bid(listing=listing_id, bid=new_bid)
            higher_bid.save()
            msg = "Bid placed successfully!"
        else:
            msg = "Can't place a bid that is lower than the previous bids."

        return render(request, "auctions/listing-page.html", {
                "listing": listing,
                "msg": msg
            })

    return render(request, "auctions/listing-page.html", {
        "listing": listing,
    })
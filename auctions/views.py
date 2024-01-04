import re
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateListingForm
from .helpers import (
    message,
    getListing,
    getWinnerId,
    getComments,
    getCategoryList,
    getSearchResults,
)
from .models import (
    User,
    Listing,
    Bid,
    Comment,
    CATEGORIES,
    Watchlist,
    Winners,
    Category,
)


def index(request):
    # Get all the currently active listings
    all_listings = Listing.objects.filter(active=True)
    return render(
        request,
        "auctions/index.html",
        {
            "all_listings": all_listings,
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            message(request, "s", "Successfully logged in!")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    message(request, "s", "Successfully logged out.")
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # Get the information from registration form
        username, email, firstname, lastname = (
            request.POST["username"],
            request.POST["email"],
            request.POST["first-name"],
            request.POST["last-name"],
        )

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            message(request, "w", "Passwords must match.")
            return render(
                request,
                "auctions/register.html",
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, first_name=firstname, last_name=lastname
            )
            user.save()
        except IntegrityError:
            message(request, "w", "Username already taken.")
            return render(
                request,
                "auctions/register.html",
            )
        # Log user in and redirect to the homepage.
        login(request, user)
        message(request, "s", "Registration successfull")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        # Create form instance and populate it with the data from the request
        form = CreateListingForm(request.POST)

        # Check whether the form is valid
        if form.is_valid():
            # Create new listing object
            new_listing = Listing(
                item=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data["start"],
                date=datetime.datetime.now(),
                user=request.user,
                current_price=0,
                image=form.cleaned_data["imgUrl"],
                active=True,
                category=form.cleaned_data["category"],
                number_of_bids=0,
            )
            new_listing.save()

            # Add new entry in categories overview table
            cat = Category(
                category_name=form.cleaned_data["category"], item=new_listing
            )
            cat.save()
            message(request, "s", "Listing created.")
            return HttpResponseRedirect(reverse("index"))
        else:
            message(request, "w", "Invalid form")
            return render(
                request,
                "auctions/create.html",
                {
                    "form": form,
                },
            )
    else:
        form = CreateListingForm()
        return render(
            request,
            "auctions/create.html",
            {
                "form": form,
            },
        )


def listing(request, id):
    ## Initialise some local variables
    current_listing = getListing(id)  # Current listing
    current_user = request.user  # Current user
    watchlisted = False  # Boolean variable indicating if the current user who wants to access the listing, already watchlisted this item
    watchlist_id = None  # Watchlist id
    is_owner = False  # Boolean variable indicating if the current user who wants to access the listing, is the one who posted the listing

    ## Get the current winner of this listing. If there are no bids on this item yet, set the current winner to None
    current_winner = getWinnerId(current_listing)

    ## Get all the commments for this listing
    all_comments = getComments(current_listing)

    # For authenticated users:
    if current_user.is_authenticated:
        # Check if this item is already in this users watchlist. If so, set the appropriate variables
        watchlistItem = current_user.my_watchlist.all().filter(
            item_id=current_listing.id
        )
        if watchlistItem.exists():
            watchlisted = True
            watchlist_id = watchlistItem[0].id

        # Check if the current user posted this listing
        if current_listing.user == current_user:
            is_owner = True
        else:
            pass

        return render(
            request,
            "auctions/listing.html",
            {
                "listing": current_listing,
                "watchlisted": watchlisted,
                "watchlist_id": watchlist_id,
                "is_owner": is_owner,
                "current_winner": current_winner,
                "user": current_user,
                "all_comments": all_comments,
            },
        )

    else:
        return render(
            request,
            "auctions/listing.html",
            {
                "listing": current_listing,
                "watchlisted": watchlisted,
                "watchlist_id": None,
                "all_comments": all_comments,
                "user": current_user,
                "current_winner": current_winner,
            },
        )


@login_required
def bid(request, id):
    listing = getListing(id)
    current_user = request.user

    # Check that the user trying to bid is not the owner of the current listing
    if current_user == listing.user:
        message(request, "w", "You can't bid on your own listing")
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    else:
        if request.method == "POST":
            user_bid = int(request.POST["bid"])

            # Check if what the user wants to bid is bigger than minimum and current price.
            # If so, create an entry in bid table to rememeber the highest bidder for this listing
            if user_bid > listing.current_price and user_bid > listing.starting_bid:
                # Save the new bid as the current price of this listing and increase by 1 the amount of bids this listing has
                listing.current_price = user_bid
                listing.number_of_bids += 1
                listing.save()

                # Save the current user's bid
                new_bid = Bid(
                    item=listing,
                    user=current_user,
                    amount=user_bid,
                    date=datetime.datetime.now(),
                )
                new_bid.save()

            else:
                message(
                    request,
                    "w",
                    "The bid must be higher than the minimum bid and the current highest bid",
                )

            message(request, "s", "Bid successfully placed!")
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            return HttpResponse("You can bid on a listing on its listing page")


@login_required
def watchlist_add(request, item_id):
    # Create a Watchlist instance with the current user as user, and the current's page item as item.
    current_listing = getListing(item_id)
    current_user = request.user

    watchlist_item = Watchlist()
    watchlist_item.user = current_user
    watchlist_item.item = current_listing
    watchlist_item.save()

    message(request, "s", "Item added to your watchlist")
    return redirect(reverse("listing", args=[item_id]))


@login_required
def watchlist_remove(request, watchlist_id):
    watchlist_entry = Watchlist.objects.get(pk=watchlist_id)
    listing_id = watchlist_entry.item.id
    watchlist_entry.delete()
    message(request, "s", "Item removed from watchlist")
    return redirect(reverse("listing", args=[listing_id]))


@login_required
def close(request, id):
    current_user = request.user
    current_listing = getListing(id)
    if request.method == "POST":
        # First, check if there are any bids on this auction
        if current_listing.number_of_bids > 0:
            # Check that the current user is the owner of the listing
            if current_listing.user == current_user:
                # Get the id of the winner of the auction
                winner = int(request.POST["winner"])

                # Create new entry in the winner table
                entry = Winners(
                    user=User.objects.get(pk=winner), listing=current_listing
                )
                entry.save()

                # Put the listing on not active
                current_listing.active = False
                current_listing.save()
                message(request, "s", "Auction closed!")
                return HttpResponseRedirect(reverse("index"))

            else:
                message(
                    request,
                    "w",
                    "You're not allowed to close this listing!",
                )
                return HttpResponseRedirect(
                    reverse("listing", args=[current_listing.id])
                )
        else:
            message(
                request,
                "w",
                "This auction cannot be closed, there are no bids on it. You can delete the listing in your profile page.",
            )
            return HttpResponseRedirect(reverse("listing", args=[current_listing.id]))
    else:
        message(
            request,
            "w",
            "Use the close option on your listings page to close the listing.",
        )
        return HttpResponseRedirect(reverse("listing", args=[current_listing.id]))


@login_required
def comment(request, id):
    if request.method == "POST":
        comment = request.POST["comment"]
        commenter_id = request.POST["user"]

        new_comment = Comment(
            item=Listing.objects.get(pk=id),
            comment=comment,
            user=User.objects.get(pk=commenter_id),
            time=datetime.datetime.now(),
        )
        new_comment.save()
        return redirect(reverse("listing", args=[id]))


@login_required
def watchlist(request):
    current_user = request.user
    watchlist = current_user.my_watchlist.all()
    bids = current_user.my_bids.all()

    return render(
        request,
        "./auctions/watchlist.html",
        {
            "watchlist": watchlist,
            "bids": bids,
        },
    )


def categories(request):
    return render(
        request,
        "auctions/category.html",
        {
            "categories": CATEGORIES,
        },
    )


def categoryList(request, category):
    # Get all the items in this category
    list = getCategoryList(category)
    readable_name = "This category doesn't exist"
    for cat in CATEGORIES:
        if cat[0] == category:
            readable_name = cat[1]

    # Render the appropriate html template
    return render(
        request,
        "./auctions/categoryList.html",
        {
            "categories": CATEGORIES,
            "items": list,
            "category": readable_name,
        },
    )


def search(request):
    if request.method == "POST":
        # Get the search query and the category, if any is selected
        query = request.POST["search_query"]
        category = request.POST["search_category"]
        category_readable = "None"
        for cat in CATEGORIES:
            if cat[0] == category:
                category_readable = cat[1]

        if category == "None":
            category_results = Listing.objects.all()
        else:
            category_results = Listing.objects.filter(category=category)

        search_results = getSearchResults(query, category_results)

        return render(
            request,
            "auctions/search.html",
            {
                "results": search_results,
                "query": query,
                "category": category_readable,
            },
        )
    else:
        return render(request, "auctions/search.html")


@login_required
def edit(request, id):
    listing = getListing(id)
    old_category = listing.category
    if request.method == "POST":
        # Create form instance and populate it with the data from the request
        createForm = CreateListingForm(request.POST)

        # Check whether the form is valid
        if createForm.is_valid():
            # Modify the existing listing
            listing.item = createForm.cleaned_data["title"]
            listing.description = createForm.cleaned_data["description"]
            listing.starting_bid = int(createForm.cleaned_data["start"])
            listing.image = createForm.cleaned_data["imgUrl"]
            listing.category = createForm.cleaned_data["category"]
            listing.save()

            # If category changed, modify the categories table
            if old_category != listing.category:
                # Delete the old category of the listing in the categories table
                old_item = Category.objects.get(item=listing)
                old_item.delete()

                # Add new entry in categories overview table
                cat = Category(
                    category_name=createForm.cleaned_data["category"], item=listing
                )
                cat.save()
            message(request, "s", "Listing modified.")
            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            message(request, "w", "Invalid form")
            return render(
                request,
                "auctions/create.html",
                {
                    "form": createForm,
                },
            )

    else:
        listingForm = CreateListingForm(
            {
                "title": listing.item,
                "description": listing.description,
                "start": listing.starting_bid,
                "imgUrl": listing.image,
                "category": listing.category,
            }
        )
        return render(
            request,
            "auctions/edit.html",
            {"form": listingForm, "id": id, "listing": listing},
        )


@login_required
def profile(request):
    current_user = request.user

    # Get all the listings that this user created
    user_listings = current_user.my_listings.all()

    # Get all the auctions this user won
    user_wins = current_user.my_wins.all()

    # Get bidding history for this user
    user_bids = current_user.my_bids.all()

    return render(
        request,
        "auctions/profile.html",
        {
            "user": current_user,
            "listings": user_listings,
            "wins": user_wins,
            "bids": user_bids,
        },
    )

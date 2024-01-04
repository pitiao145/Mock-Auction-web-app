import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from typing import List, Dict
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


## Helper functions
def message(request, type, message):
    if type == "w":
        return messages.add_message(request, messages.WARNING, message)
    elif type == "s":
        return messages.add_message(request, messages.SUCCESS, message)


## Queries
def getListing(id: int) -> Listing:
    """Queries a listing based on its id"""
    return Listing.objects.get(pk=id)


def getWinnerId(item: Listing) -> int:
    """Get the id of the current winner of an item. Checks if there's is a winner before queriing the database.
    Returns None if there is no winner"""
    return (
        Bid.objects.filter(item=item).order_by("-amount")[:1][0].user.id
        if Bid.objects.filter(item=item).exists()
        else None
    )


def getComments(listing: Listing) -> List[Comment]:
    """Gets all the comments for a specific listing, ordered by the most recent listing first"""
    return Comment.objects.filter(item=listing).order_by("-time")


def getCategoryList(category: str) -> List[Category]:
    """Return a list of all Category objects (category_name and item) for a certain category"""
    return set(Category.objects.filter(category_name=category))


## Search query using regex
def getSearchResults(query: str, list: List[Listing]) -> List[Listing]:
    """Return a list of listings that matches a search query. Takes as input
    a search query and the list in which the results should be looked up."""
    results = []
    for result in list:
        if matches := re.search(f"^.*{query.lower()}.*$", result.item.lower()):
            results.append(result)
    return results

from .models import User, Listing, Bid, Comment, CATEGORIES, Watchlist, Winners, Category


def add_variable_to_context(request):
    return {
        'categories': CATEGORIES,
    }
from django.contrib import admin

# Register your models here.

from .models import Listing, Bid, Comment, User, Watchlist, Winners, Category

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "user", "current_price", "number_of_bids", "active")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "user", "comment")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item")

class WinnerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "item_id")    
    
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Winners, WinnerAdmin)
admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from .models import Listing, User, Category, Bid, Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "start_bid", "image_url", "category", "highest_bidder", "active")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "comment", "user")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bid")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)

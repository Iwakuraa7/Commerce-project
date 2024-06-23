from django.contrib import admin
from .models import Listing, User, Category, Bid, Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "start_bid", "image_url", "category", "user", "highest_bidder")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)

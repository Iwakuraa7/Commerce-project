from django.contrib import admin
from .models import Listing, User, Category, Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "start_bid", "image_url", "category")

admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)

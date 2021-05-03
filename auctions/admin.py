from django.contrib import admin
from .models import User,Category,Listing,Bid,Comment,Winner
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title","text","bs_bid","img","owner","category","active","datefield")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("text","listing","user","datetime")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing,ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Winner)
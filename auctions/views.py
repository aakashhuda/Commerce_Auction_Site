from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .forms import AddListing,BidForm,UpdateListingForm,CommentForm
from .models import User,Category,Listing,Bid,Comment
from django.core.exceptions import EmptyResultSet


def index(request):
    try:
        user = User.objects.get(username=request.user)
        count = user.user_watchlist.all().count()
    except:
        count = 0
    try:
        listings = Listing.objects.all()
    except:
        return render(request, "auctions/index.html",{
            "count":count,
        })
    categories = Category.objects.all()
    
    return render(request, "auctions/index.html",{
        "listings":listings,
        "categories":categories,
        "count":count,
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
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('auctions:index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auctions:index'))


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
        return HttpResponseRedirect(reverse('auctions:index'))
    else:
        return render(request, "auctions/register.html")
@login_required(login_url='auctions:login')
def add_listing(request):
    user = User.objects.get(username=request.user)
    count = user.user_watchlist.all().count()
    form = AddListing()
    print(request.user.id)
    return render(request, "auctions/add_listing_form.html", {
        "form":form,
        "count":count,
    })
@login_required(login_url='auctions:login')
def save_listing(request):
    if request.method == 'POST':
        form = AddListing(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            bs_bid = form.cleaned_data["bs_bid"]
            img = form.cleaned_data["img"]
            cat = form.cleaned_data["category"]
            try:
                check_cat = Category.objects.get(cat_name=cat.title())
                print(check_cat)
            except:
                new_category = Category(cat_name = cat.title())
                new_category.save()
                print(new_category)
                new_listing = Listing(title = title.title(),text=text,bs_bid=bs_bid,img=img,category=new_category,
                owner=request.user)
                new_listing.save()
                return HttpResponseRedirect(reverse("auctions:index"))
            new_listing = Listing(title = title.title(),text=text,bs_bid=bs_bid,img=img,category=check_cat,
            owner=request.user)
            new_listing.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            user = User.objects.get(username=request.user)
            count = user.user_watchlist.all().count()
            return render(request, "auctions/add_listing_form.html",{
                "form":form,
                "message": "Invalid Request! Fill up and submit the form again.",
                "count":count,
            })
    user = User.objects.get(username=request.user)
    count = user.user_watchlist.all().count()     
    return render(request, "auctions/add_listing_form.html",{
        "form":AddListing(),
        "message": "Invalid Request! Fill up and submit the form!.",
        "count":count,
        
        
    })
@login_required(login_url='auctions:login')
def listing_details(request,title):
    user = User.objects.get(username=request.user)
    count = user.user_watchlist.all().count()
    try:
        listing = Listing.objects.get(title=title.title())
    except Listing.DoesNotExist:
        return render(request, "auctions/listing_details.html",{
            "no_item_message":"Item not available",
            "title":title,
            "count":count,
        })
    comments = Comment.objects.filter(listing=listing).order_by('-datetime').all()
    try:
        hs_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
    except Bid.EmptyResultSet:
        return render(request, "auctions/listing_details.html",{
            "listing":listing,
            "title":title,
            "form":BidForm(),
            "listing_form": UpdateListingForm(instance=listing),
            "comment_form":CommentForm(),
            "comments":comments,
            "count":count,
        })
    if hs_bid is not None:
        data = {"amount":hs_bid.amount}          
        return render(request, "auctions/listing_details.html",{
            "listing":listing,
            "title":title,
            "hs_bid":hs_bid,
            "form":BidForm(initial=data),
            "listing_form": UpdateListingForm(instance=listing),
            "comment_form":CommentForm(),
            "comments":comments,
            "count":count,
        })
    else:
        return render(request, "auctions/listing_details.html",{
            "listing":listing,
            "title":title,
            "hs_bid":hs_bid,
            "form":BidForm(),
            "listing_form": UpdateListingForm(instance=listing),
            "comment_form":CommentForm(),
            "comments":comments,
            "count":count,
        })  

@login_required(login_url='auctions:login')
def post_bid(request):
    if request.method == 'POST':
        listing_info = request.POST["listing_info"]
        print(listing_info)
        listing = Listing.objects.get(title=listing_info)
        bid_form = BidForm(request.POST)
        list_activation = UpdateListingForm(request.POST)

        if bid_form.is_valid():
            amount = bid_form.cleaned_data["amount"]
            watchlist = bid_form.cleaned_data["watchlist"]
            remove_watchlist = bid_form.cleaned_data["remove_watchlist"]
            print(f"watchlist: {watchlist}")
            if amount is not None:
                hs_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
                if hs_bid is not None:
                    if amount > hs_bid.amount and amount > listing.bs_bid:
                        bid = Bid(listing=listing,user=request.user,amount=amount)
                        bid.save()
                    else:
                        print(hs_bid)
                        return render(request, "auctions/listing_details.html",{
                            "message": "Bid must be greater than the Base price & Highest Bid",
                            "listing":listing,
                            "hs_bid":hs_bid,
                            "title": listing.title,
                            "form":BidForm(request.POST),
                            "listing_form":UpdateListingForm(request.POST),
                            "comment_form":CommentForm(),
                        })
                else:
                    if amount > listing.bs_bid:
                        bid = Bid(listing=listing, user =request.user, amount=amount)
                        bid.save()
                    else:
                        return render(request, "auctions/listing_details.html",{
                            "message": "Bid must be greater than the Base price & Highest Bid",
                            "listing":listing,
                            "hs_bid":hs_bid,
                            "title": listing.title,
                            "form":bid_form,
                            "listing_form":list_activation,
                            "comment_form":CommentForm(),
                        })

            if watchlist is True:
                listing.watchlist.add(request.user)
            if remove_watchlist is True:
                listing.watchlist.remove(request.user)
        else:
            return HttpResponse('Bid form not Ok')
        
        if list_activation.is_valid():
            active = list_activation.cleaned_data["active"]
            print(f"listactivations: {active}")
            if active is False:
                listing.active = False
                listing.save()
                return HttpResponseRedirect(reverse('auctions:index'))
            else:
                listing.active = True
                listing.save()
                return HttpResponseRedirect(reverse('auctions:index'))
        else:
            return HttpResponse('list activation failed')
    return HttpResponseRedirect(reverse('auctions:index'))

def save_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            print(comment)
            listing_name = request.POST['listing']
            user = request.user
            listing = Listing.objects.get(title=listing_name)
            new_comment = Comment(user=user,listing=listing,text=comment)
            new_comment.save()
            return HttpResponseRedirect(reverse('auctions:listing_details', kwargs={'title':listing.title.title()}))

        else:
            user = User.objects.get(username=request.user)
            count = user.user_watchlist.all().count()
            return render(request, "auctions/listing_details",{
                "listing":listing,
                "title":title,
                "hs_bid":hs_bid,
                "form":BidForm(initial=data),
                "listing_form": UpdateListingForm(instance=listing),
                "comment_form":form,
                "message":"Form not Valid! Comment Again",
                "count":count,
            })
    else:
        return HttpResponseRedirect(reverse("auctions:index"))
@login_required(login_url='auctions:login')
def categorized_listings(request,category):
    user = User.objects.get(username=request.user)
    count = user.user_watchlist.all().count()
    try:
        category = Category.objects.get(cat_name=category.title())
    except Category.DoesNotExist:
        return render(request, 'auctions/category_listings.html',{
            'message':f"Invalid query.{category.title()} doesn't exist",
            'count':count,
        })
    listings = category.category_listing.all()
    if listings is None:
        return render(request, 'auctions/category_listings.html',{
            "message": "No listing available!",
            "count":count,
        })
    else:
        return render(request, 'auctions/category_listings.html',{
            "listings":listings,
            "count":count,
        }) 
@login_required(login_url='auctions:login')
def watchlist(request,user):
    print(request.user)
    print(user)
    if user == str(request.user):
        try:
            user_object = User.objects.get(username=user)
        except User.DoesNotExist:
            return render(request, 'auctions/watchlist.html',{
                "message": f"{user.title()} doesn't exist!"
            })
        watchlist = user_object.user_watchlist.all()
        return render(request, 'auctions/watchlist.html',{
            "watchlist":watchlist,
        })
    else:
        return render(request, "auctions/watchlist.html",{
            "message": "You are not allowed to see others watchlist!"
        })
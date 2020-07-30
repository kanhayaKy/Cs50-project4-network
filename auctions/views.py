from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing , Bid ,Comment , Watchlist ,User
from .forms import createListingForm


def index(request):

    return render(request, "auctions/index.html",{
        "listing" : Listing.objects.all(),
        "categories": Listing.objects.values('category').distinct(),

    })

def inactive(request):
    return render(request, 'auctions/inactivelist.html',{
        "inactive":Listing.objects.filter(isactive = False)
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




@login_required()
def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = createListingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data['title']
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            if category:
                category = category.capitalize()
            try:
                listing = Listing(user = request.user , title = title , description = description, starting_bid = bid ,category = category, image_url = url )
                listing.save()
            except Exception:
                return render(request , "auctions/create.html", {
                    "message":"Please Try Again"
                })
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request , "auctions/create.html", {
                    "form":form
                })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = createListingForm()
        return render(request , "auctions/create.html", {
                    "form":form,
                })




def listing(request,number,message=""):
    item = Listing.objects.get(id=number)
    max_bid = Bid.objects.filter(listing = item).aggregate(Max('bid'))['bid__max']
    try:
        item.bidder = Bid.objects.filter(listing = item , bid = max_bid)[0].user
    except:
        pass
    
    return render(request,"auctions/listing.html",{
        "item":item,
        "current_bid":max_bid,
        "count":Bid.objects.filter(user = item.user).count(),
        "comments":Comment.objects.filter(listing = item),
        "message":message
        
    })


def category(request, category):
    items = Listing.objects.filter(category=category)
    return render(request,"auctions/category.html",{
        "items":items
    })

@login_required()
def WatchList(request,item=None):
    user = request.user
    if request.method == 'POST':
        listing = Listing.objects.get(pk=item)
        if Watchlist.objects.filter(user = user , listing = listing):
            Watchlist.objects.filter(user = user , listing = listing).delete()
            return HttpResponseRedirect(reverse('listing',args=[item,"Removed from watch list"]))
            
        else:
            watchlist = Watchlist(user = user , listing = listing)
            watchlist.save()
            return HttpResponseRedirect(reverse('listing',args=[item,"Added to watch list"]))


    list = Watchlist.objects.filter(user = user)
    return render(request,'auctions/watchlist.html',{
        "watchlist": list
    })


@login_required()
def addBid(request,list):
    listing = Listing.objects.get(pk=list)
    if listing.isactive:
        user = request.user
        bid = float(request.POST['bid'])
        max_bid = Bid.objects.filter(listing = listing).aggregate(Max('bid'))['bid__max']

        if bid > listing.starting_bid :
            if bid is not None or bid > max_bid:
                new_bid = Bid(user=user,bid=bid,listing=listing)
                new_bid.save()

            return HttpResponseRedirect(reverse('listing',args=[list]))
        else:
            return HttpResponseRedirect(reverse('listing',args=[list,"You have to Bid higher than that"]))
   
    else:
        return HttpResponseRedirect(reverse('listing',args=[list,"This listing has been closed"]))


@login_required()
def closeBid(request,number):
    listing = Listing.objects.get(pk=number)
    listing.isactive = False
    listing.save()
    print(listing.isactive, listing.title)
    return HttpResponseRedirect(reverse('listing',args=[number,"This listing has been closed"]))

@login_required()
def comment(request,number):
    listing = Listing.objects.get(pk=number)
    comment = request.POST['comment']
    newComment = Comment(user = request.user , listing = listing , comment = comment )
    try:
        newComment.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(reverse('listing',args=[number]))
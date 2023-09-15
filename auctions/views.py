import pathlib
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *


def index(request):

    active_listings = Listing.objects.filter(status="a")
    watchlist_count = Watchlist.objects.filter(user=request.user.id).count()
    my_listings_count = Listing.objects.filter(user=request.user.id).count()

    return render(
        request,
        "auctions/index.html",
        {
            "listings": active_listings,
            "message1": "Active listings",
            "message2": "No active listings",
            "flag": "index",
            "watchlist_count": watchlist_count,
            "my_listings_count": my_listings_count,
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
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def create_listing(request):

    if request.method == "POST":

        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():

            listing = Listing()
            now = datetime.now()

            listing.datetime = now
            listing.user = User.objects.get(pk=request.user.id)
            listing.title = form.cleaned_data["title"]
            listing.starting_bid = form.cleaned_data["starting_bid"]
            listing.category = form.cleaned_data["category"]
            listing.image_url = form.cleaned_data["image_url"]
            listing.description = form.cleaned_data["description"]
            listing.current_price = listing.starting_bid

            try:
                # 'try' statement is succesful if user downloads any file in create_listing page
                file_uploaded = request.FILES["file"]
                file_uploaded_name = file_uploaded.__str__()

                # uploaded file validation by its extention
                # for valid stand extentions of three image formats
                # which are valid for <img> HTML tag
                if (
                    file_uploaded_name.lower().endswith(".jpg")
                    or file_uploaded_name.lower().endswith(".jpeg")
                    or file_uploaded_name.lower().endswith(".png")
                    or file_uploaded_name.lower().endswith(".gif")
                ):

                    # case of uploaded file with valid extension
                    # filename constructor is specified to guarantee uniqueness
                    # datetime.now() cast to string
                    listing.filename = (
                        request.user.username
                        + now.strftime("_%d_%m_%Y_at_%H_%M_%S_")
                        + file_uploaded_name
                    )
                    name_to_save = "auctions/images/" + listing.filename
                else:
                    # case of uploaded file with invalid extention
                    # even though some file was uploaded, we overwrite file_uploaded to False
                    # to prevent saving of this file to disk
                    file_uploaded = False
                    name_to_save = " "
                    # filling the  filename field of Listing class in case of invalid file extention
                    listing.filename = (
                        request.user.username
                        + now.strftime("_%d_%m_%Y_at_%H_%M_%S_")
                        + "no_file"
                    )

            except KeyError:
                # the case when no file was uploaded
                file_uploaded = False
                name_to_save = " "
                # filling the Listing filename field in case of no file uploaded
                listing.filename = (
                    request.user.username
                    + now.strftime("_%d_%m_%Y_at_%H_%M_%S_")
                    + "no_file"
                )

            # writing down uploaded file to disk in case  if it exists and has valid extention
            if file_uploaded:
                handle_uploaded_file(file_uploaded, name_to_save)

            try:
                listing.save()

                return HttpResponseRedirect(
                    reverse("listing_page", args=(listing.id, name_to_save, " "))
                )
            except:
                # case of , say, overflow in price field or some other error in user malicious input
                form = CreateListingForm()
                return render(
                    request,
                    "auctions/create_listing.html",
                    {"form": form, "message": "Invalid input, try again"},
                    )

        else:
            form = CreateListingForm()
            return render(
                request,
                "auctions/create_listing.html",
                {"form": form, "message": "Invalid input, try again"},
            )

    else:
        form = CreateListingForm()
        watchlist_count = Watchlist.objects.filter(user=request.user.id).count()
        my_listings_count = Listing.objects.filter(user=request.user.id).count()
    return render(
        request,
        "auctions/create_listing.html",
        {
            "form": form,
            "message": "",
            "watchlist_count": watchlist_count,
            "my_listings_count": my_listings_count,
        },
    )


def handle_uploaded_file(f, name):
    """
    Helper func - writes down the uploaded file to 'auctions/static/ folder
    """
    with open("auctions/static/" + name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def listing_page(request, listing_id, name_to_save, message):

    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        # exception may occur if user tries manually url like this
        # listing_page/SOME_NUMBER/SOME_STRING/SOME_STRING
        # where SOME_NUMBER is a number that is not equal to any
        # of existing Listing class instances' id
        return render(request, "auctions/not_found.html")

    if request.method == "POST":
        form = CommentForm(request.POST)

        try:
            if form.is_valid():
                content = form.cleaned_data["comment"]
                comment = Comment(user=request.user, listing=listing, content=content)
                comment.save()
        except:
            # case of malicious client side html editing - comment will be ignored
            pass

    # overwrites name_to_save variable in case when listing_page view
    # was called from 'index.html' template by a link to Listing instance
    # which contains no real file bound
    # That is being done to prevent image rendering of not existing file
    if name_to_save.endswith("no_file"):
        name_to_save = " "

    bid_form = BidForm()
    comment_form = CommentForm()

    bid_count = Bid.objects.filter(listing=listing).count()
    watchlist_count = Watchlist.objects.filter(user=request.user.id).count()
    my_listings_count = Listing.objects.filter(user=request.user.id).count()
    comments = Comment.objects.filter(listing=listing)

    # specifies appearance of description frame in template
    if len(listing.description) > 200:
        long_description = True
    else:
        long_description = False

    return render(
        request,
        "auctions/listing_page.html",
        {
            "listing": listing,
            "name_to_save": name_to_save,
            "bid_form": bid_form,
            "comment_form": comment_form,
            "message": message,
            "bid_count": bid_count,
            "watchlist_count": watchlist_count,
            "my_listings_count": my_listings_count,
            "comments": comments,
            "long_description": long_description,
        },
    )


def not_found(request, anything):
    return render(request, "auctions/not_found.html")


@login_required(login_url="/login")
def watchlist(request, action):

    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])
        try:
            listing = Listing.objects.get(pk=listing_id)
        except:
            # Case of malicious client side html editing
            message = "Access denied "
            return render(request, "auctions/message.html", {"message": message})

        if action == "remove":
            # deleting Watchlist instance
            Watchlist.objects.filter(user=request.user, listing=listing)[0].delete()
        elif action == "add_to_watchlist":
            try:
                # checks if such Watchlist instance already exists
                watchlist = Watchlist.objects.filter(
                    user=request.user, listing=listing
                )[0]
            except:
                # creates an instance if not yet exists
                watchlist = Watchlist(user=request.user, listing=listing)
                watchlist.save()
        else:
            # Case of malicious client side html editing
            message = "Access denied"
            return render(request, "auctions/message.html", {"message": message})

    # reconstruction of sequence of Listing instances
    # that compose watchlist
    watchlist = Watchlist.objects.filter(user=request.user)
    listings = []
    for item in watchlist:
        listings.append(item.listing)

    watchlist_count = Watchlist.objects.filter(user=request.user).count()
    my_listings_count = Listing.objects.filter(user=request.user).count()
    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
            "message1": "Watchlist",
            "message2": "No items in watchlist",
            "flag": "watchlist",
            "watchlist_count": watchlist_count,
            "my_listings_count": my_listings_count,
        },
    )


@login_required(login_url="/login")
def add_bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)

            # path to retrieve image file from disk
            image_path = "auctions/images/" + listing.filename
        except:
            # Case of malicious client side html editing
            message = "Access denied"
            return render(request, "auctions/message.html", {"message": message})

        form = BidForm(request.POST)
        try:
            if form.is_valid():
                new_bid = form.cleaned_data["new_bid"]

                if new_bid <= listing.current_price:
                    message = "New bid must be bigger than current price"
                else:
                    bid = Bid(user=request.user, listing=listing, amount=new_bid)
                    listing.current_price = new_bid
                    listing.current_bidder = request.user.username
                    bid.save()
                    listing.save()
                    message = " "
            else:
                # Case of malicious client side html editing
                message = "Invalid input 1"
        except:
            message = "Invalid input 2"
        return HttpResponseRedirect(
            reverse("listing_page", args=(listing.id, image_path, message))
        )
    else:
        return HttpResponseRedirect("not_found")


@login_required(login_url="/login")
def my_listings(request, action):

    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])

        try:
            listing = Listing.objects.get(pk=listing_id)
        except:
            # case of malicious client side html editing
            message = "Access denied"
            return render(request, "auctions/message.html", {"message": message})

        # check if listing, got by POST, really belongs to user loged in
        # that can be violated in case of malicious client side html editing
        if listing.user.id != request.user.id:
            message = "Access denied"
            return render(request, "auctions/message.html", {"message": message})

        if action == "close":
            listing.status = "n"
            listing.save()

            # including  listing to winner's whatchlist if it is not already there
            try:
                # User instance - if exists - the auction winner
                winner = listing.bids.get(amount=listing.current_price).user

                try:
                    # check if the winner already has the listing in his watchlist
                    watchlist = Watchlist.objects.filter(user=winner, listing=listing)[
                        0
                    ]
                except:
                    # the winner forgot to include to his watchlist the listing, that he bids on
                    # after closing a listing there is the only way to get non active listing
                    # it is trough  personal watchlist of a user
                    # here the listing is being inserted to the winner's watchlist
                    watchlist = Watchlist(user=winner, listing=listing)
                    watchlist.save()
            except:
                # case of no Bid instances for this listing -therefor no winner
                pass
        elif action == "delete":
            # first deleting image file from disk if exists, then deleting Listing instance itself

            # check if an image file was bound while Listing instance was created
            if not listing.filename.endswith("no_file"):
                file_to_delete = "auctions/static/auctions/images/" + listing.filename
                try:
                    # deleting  file from disk
                    pathlib.Path(file_to_delete).unlink()
                except:
                    # file not found - no action is being done
                    pass
            listing.delete()
        else:
            # Case of malicious client side html editing
            message = "Access denied"
            return render(request, "auctions/message.html", {"message": message})

    user_id = request.user.id
    listings = Listing.objects.filter(user=user_id)
    my_listings_count = listings.count()
    watchlist_count = Watchlist.objects.filter(user=user_id).count()

    # compose list of tuples. Each tuple contains listing id and a query result
    # with all bids, related to  this listing
    bids_for_my_listings = []
    for listing in listings:
        bids_for_my_listings.append((listing.id, listing.bids.all()))

    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
            "message1": "My listings",
            "message2": "No listing has been hosted yet",
            "flag": "my_listings",
            "user_id": user_id,
            "watchlist_count": watchlist_count,
            "my_listings_count": my_listings_count,
            "bids_for_my_listings": bids_for_my_listings,
        },
    )


def categories(request, action, category):

    watchlist_count = Watchlist.objects.filter(user=request.user.id).count()
    my_listings_count = Listing.objects.filter(user=request.user.id).count()

    if action == "to_content":
        listings_categorized = Listing.objects.filter(category=category)
        return render(
            request,
            "auctions/index.html",
            {
                "listings": listings_categorized,
                "message1": "Category: " + category,
                "message2": "No listings in category " + category,
                "flag": "category",
                "watchlist_count": watchlist_count,
                "my_listings_count": my_listings_count,
            },
        )

    return render(
        request,
        "auctions/categories.html",
        {
            "categories": category_choices,
            "watchlist_count": watchlist_count,
            "my_listings_count": my_listings_count,
        },
    )

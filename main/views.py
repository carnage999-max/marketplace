import random
import string
import time

import cloudinary.uploader
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import *
from .models import *

categories = []
for i in CATEGORY:
    categories.append(i[1])

mail = 'jamesezekiel039@gmail.com'


# ----------- HomePage -------- #
def index(request):
    products = Product.objects.all().order_by("-date_added")
    urls = CloudinaryURLs.objects.all()
    for url in urls:
        print(url.productt)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/index.html', context)


# --------------------------- Login and signup -------------------- #
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = RegistrationForm()
    return render(request, 'main/signup.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Email or Password is incorrect!')
    else:
        form = SignInForm()

    return render(request, 'main/signin.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('login'))


@login_required(login_url='login')
def UserProfile(request, username):
    user_details = CustomUser.objects.get(username=username)
    user_products = Product.objects.filter(retailer=user_details)
    return render(request, 'main/profile.html', {"user": user_details, "user_products": user_products})


@login_required(login_url='login')
def updateProfile(request, username):
    user_profile = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()     
            # Redirect to the profile page after successful update
            return redirect('profile', username=username)
    else:
        form = UpdateProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'main/update-profile.html', context)


# ---------------------------End of Login and signup --------------------#

@login_required(login_url='login')
def AddProduct(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        retailer = request.user
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            product_description = form.cleaned_data['product_description']
            images = request.FILES.getlist('product_image')
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']
            user = CustomUser.objects.get(username=retailer)
            num_ads = user.num_ads
            product = Product(
            product_name=product_name,
            retailer=retailer,
            product_description=product_description,
            product_image=images[0],
            price=price,
            quantity=quantity, category=category,
            sub_category=sub_category,
        )
            for image in images:
                result = cloudinary.uploader.upload(image)
                url = CloudinaryURLs(
                productt=product, 
                link=result['url'],
            )
                product.save()
                url.save()
            num_ads = num_ads + 1
            return redirect('index')
    else:
        form = AddProductForm()
    return render(request, "main/addproduct.html", {'form': form})


def productDescription(request, pk):
    product_detail = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product=pk)
    urls = CloudinaryURLs.objects.filter(productt=pk)
    num_review = len([review for review in reviews])
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Review.objects.create(
                buyer=request.user,
                product=product_detail,
                comment=comment,
            )
            return redirect('desc', pk=pk)
    else:
        form = ReviewForm()
    related_product_name = Product.objects.filter(
        retailer=product_detail.retailer) | Product.objects.filter(category=product_detail.category)
    context = {
        "product": product_detail,
        "form": form, 'num': num_review,
        'reviews': reviews,
        "related_products": related_product_name,
        'urls':urls,
    }
    return render(request, 'main/productdesc.html', context)
 

def categoryFilter(request, category):
    filtered_products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': filtered_products,
        'categories': categories
    }
    return render(request, 'main/category_filter.html', context)


def search(request):
    products = Product.objects.all().order_by("-date_added")
    query = request.GET.get('search')
    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) | Q(category__icontains=query) | Q(sub_category__icontains=query)
            
            )
    else:
        results = None
    context = {
        "results": results,
        'products': products,
        'query': query,
    }
    return render(request, 'search-results.html', context)


def faq(request):
    return render(request, "main/faq.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(
                    f'{subject}',
                    f'\n{message}\n\nThank You.\n{name}.\n0{phone_number}.\n{email}',
                    mail,
                    [mail],
                    fail_silently=False,
                )
                messages.success(request, "Message sent successfully")
            except:
                return HttpResponse("An error occured! Try again later...")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {"form": form})


def terms(request):
    return render(request, "main/t-and-c.html")


def about(request):
    return render(request, "main/about.html")


def privacy(request):
    return render(request, "main/privacy_policy.html")


@login_required(login_url='login')
def reportIssue(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['issue']
            try:
                send_mail(
                    f'{subject}',
                    f'\n{message}\n\nThank You.\n{name}.\n{phone_number}.\n{email}',
                    mail,
                    [mail],
                    fail_silently=False,
                )
                messages.success(request, "Message sent successfully")
            except:
                return HttpResponse("An error occured! Try again later...")
            return redirect('report')
    else:
        form = ReportForm()
    return render(request, "main/report-issue.html", {"form": form})


@login_required(login_url='login')
def deleteAd(request, pk):
    try:
        ad = Product.objects.get(pk=pk)
        ad.delete()
        messages.success(request, "Ad deleted successfully")
    except:
        return HttpResponse("An unexpected error occured")
    return redirect('index')


@login_required(login_url='login')
def confirmDelete(request, pk):
    ad = Product.objects.get(pk=pk)
    return render(request, 'main/confirm-delete.html', {"ad": ad})


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session with the new password
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password has been successfully updated!')
            return redirect('profile', username=request.user)
    else:
        form = ChangePasswordForm(request.user)

    context = {
        'form': form,
    }
    return render(request, 'main/change_password.html', context)


def send_message(request, recepient_id):
    recipient = get_object_or_404(CustomUser, id=recepient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            message = Message.objects.create(
                sender=request.user, recipient=recipient, content=content
                )
            return redirect('view_messages')


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(
        buyer=request.user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(buyer=request.user, product=product)
        messages.success(request, "Item Successfully added to cart!")
    return redirect('index')


@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    total_price = sum(
        item.quantity * item.product.price for  item in cart_items)
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total': total_price})


def generate_order_code():
    timestamp = int(time.time())
    random_chars = "".join(random.choices(
        string.ascii_uppercase + string.digits, k=6))
    order_code = f"{timestamp}-{random_chars}"
    return order_code


@login_required(login_url='login')
def checkout(request):
    order = Order.objects.filter(buyer=request.user).first()
    if order:
        messages.warning(request, "You already have an existing order!")
    else:
        cart_items = CartItem.objects.filter(buyer=request.user)
        total_price = sum(
            item.quantity * item.product.price for item in cart_items)
        order = Order.objects.create(
            order_code=generate_order_code(), buyer=request.user,
            total_price=total_price, is_completed=True
        )
        cart_items.delete()
    return render(request, "main/checkout.html", {'order': order})


@login_required(login_url='login')
def cancelOrder(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return redirect('index')

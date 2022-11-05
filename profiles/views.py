import json
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import UserProfile, Cart, Library
from presets.models import Preset
from django.contrib.auth.decorators import login_required
from .forms import EditProfileInformation, EditUserData, EditProfileImage, UserPasswordResetForm
#email
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import os

#paypal SDK
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError
from paypalhttp.encoder import Encoder
from paypalhttp.serializers.json_serializer import Json
import time
import string
import random

# Create your views here.

def profile(request, name):
    user = User.objects.get(username = name)
    presets = Preset.objects.all().filter(seller = user)
    userProfile, created = UserProfile.objects.get_or_create(user = user)
    
    library = Library.objects.all().filter(user = user)

    context = {
        'image': userProfile.profileImage,
        'bio': userProfile.bio,
        'user': user,
        'presets': presets,
        'i_link': userProfile.instagram_link,
        'f_link': userProfile.facebook_link,
        't_link': userProfile.tiktok_link,
        'tw_link': userProfile.twitter_link,
        'p_link': userProfile.pinterest_link,
        'library': library
    }

    return render(request, 'profiles/profile.html', context)

def settings(request, name):
    user = User.objects.get(username = name)
    profile = UserProfile.objects.get(user = user)

    if request.user != user:
        return redirect('profiles', user.username)

    form_profile_information = EditProfileInformation(instance=profile)
    form_user_data = EditUserData(instance=request.user)
    form_image = EditProfileImage(instance=profile)
 
    if request.method == 'POST':
        if request.POST.get('Update'):
            #profile information 
            form_profile_information = EditProfileInformation(request.POST, request.FILES, instance=profile)

            if form_profile_information.is_valid():
                form_profile_information.save()

                return redirect('profiles', request.user)
            else:
                print(form_profile_information.errors)

        elif request.POST.get('Save information'):
            form_user_data = EditUserData(request.POST,  instance=request.user)
            if form_user_data.is_valid():
                form_user_data.save()
            
                return redirect('profiles', request.user)
            else:
                print(form_user_data.changed_data)
                print(form_user_data.errors)

        elif request.POST.get('Save'):
            form_image = EditProfileImage(request.POST, request.FILES, instance=user)

            if form_image.is_valid():

                form_image.save()
                print(form_image.cleaned_data)

                print('bo bine')
                return redirect('profiles', request.user)
            else:
                print(form_image.changed_data)
                print(form_image.errors)
                print(form_image.data)

    context = {
        'profile': profile,
        'user': user,
        'form_generic': form_profile_information,
        'form_user': form_user_data,
        'form_image' : form_image
    }

    return render(request, 'profiles/settings.html', context)

def delete(request, name):

    user = User.objects.get(username = name)

    if request.user != user:
        return redirect('profiles', user.username)

    if request.method == 'POST':
        email = request.POST['email']

        print(user.email)
        if email == user.email:
            presets = Preset.objects.all().filter(seller = user)
            user_profile = UserProfile.objects.get(user= user)

            user_profile.profileImage.delete()
            library = Library.objects.all().filter(user = user)

            for p in presets: #delete all presets' covers and files
                p.file.delete()
                p.cover.delete()

            for p in library: 
                p.delete()
            
            #Delete account
            user.delete()  
            return redirect('home')
        else:
            print('nononos')
            pass
            #Can't delete account
            #Raise error or something

    context = {}

    return render(request, 'profiles/delete.html', context)

def password_reset_request(request):

    form = UserPasswordResetForm()

    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
    
        if form.is_valid():
    
            data = form.cleaned_data['email']
            user = User.objects.get(email = data)

            
            print(data)

            if user:
                email_template_name = 'profiles/reset_pass_msg.txt'
                parameters = {
                    'user': user,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Lightstore',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, parameters)

                '''
                message = Mail(
                from_email='lightstore23@outlook.com',
                to_emails=data,
                subject='Reset your password',
                html_content=email)
                try:
                    sg = SendGridAPIClient('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')
                    response = sg.send(message)

                    return redirect('password_reset_done')
                except Exception as e:
                    print(e)
                '''
                
           

    context = {'form': form}

    return render(request, 'profiles/password_reset.html', context)

def cart(request, name):
    user = User.objects.get(username = name)

    CartData = Cart.objects.all().filter(user = user)

    TotalPrice = 0
    products_id = []

    for item in CartData:
        TotalPrice += item.product.price
        products_id.append(item.product.id)

    context = {
        'data': CartData,
        'TotalPrice': TotalPrice,
        'products_id': products_id
        }

    return render(request, 'profiles/cart.html', context)

def payment_result(request, name):
    body = json.loads(request.body)
    products_id = json.loads(body['products_id'])
    price = json.loads(body['price'])

    price = (80 * price) / 100

    for p_id in products_id:

        #remove products from cart
        product = Preset.objects.get(id = p_id)
        item = Cart.objects.get(user = request.user, product = product)
        item.delete()

        #add product to library

        library = Library.objects.create(user = request.user, product = product).save()

        #add a new order to the total number
        profile = UserProfile.objects.get(user = product.seller)
        profile.total_orders += 1
        profile.save()

    time.sleep(5)
    paypal_payout('sellerNelu@gmail.com', price)


    return render(request, 'profiles/payment_complete.html', {})

def paypal_payout(email, amount):
    email = email

    client_id = "AW2KMsaHgBpmWPRmjXwHBSIFWLTILB_V5UCHM-qMNlh4rURfzwURad0JBJwA1WUag0lHzCvComH68Yoh"
    client_secret = "ELjzHRJkwE7sS2JXsWS3pLG1DDW9iaegYnY1-sEDBVyVGGFcu0WXRZCdZKiT_h6Rb3EeI9QcF-_PrN4-"

    environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)

    senderBatchId = str(''.join(random.sample(
            string.ascii_uppercase + string.digits, k=7)))

    body = {
    "sender_batch_header": {
        "recipient_type": "EMAIL",
        "email_message": "Preset sold",
        "note": "Enjoy your Payout!!",
        "sender_batch_id": senderBatchId,
        "email_subject": "Payment"
    },
    "items": [{
        "note": f"Your {amount}$ Payout!",
        "amount": {
            "currency": "USD",
            "value": str(amount)
        },
        "receiver": str(email),
        "sender_item_id": "Test_txn_1"
    }, ]
    }

    request = PayoutsPostRequest()
    request.request_body(body)

    try:
        # Call API with your client and get a response for your call
        response = client.execute(request)
        # If call returns body in response, you can get the deserialized version from the result attribute of the response
        batch_id = response.result.batch_header.payout_batch_id     
    except HttpError as httpe:
        # Handle server side API failure
        encoder = Encoder([Json()])
        error = encoder.deserialize_response(httpe.message, httpe.headers)
        print("Error: " + error["name"])
        print("Error message: " + error["message"])
        print("Information link: " + error["information_link"])
        print("Debug id: " + error["debug_id"])
        print("Details: ")
        for detail in error["details"]:
            print("Error location: " + detail["location"])
            print("Error field: " + detail["field"])
            print("Error issue: " + detail["issue"])

    except IOError as ioe:
        #Handle cient side connection failures
        print(ioe.message)        

@login_required(login_url='/login')
def stats(request, name):
    user = User.objects.get(username = name)
    presets = Preset.objects.all().filter(seller = user)

    if request.user != user:
        return redirect('profiles', user.username)

    profile = UserProfile.objects.get(user = request.user)

    Total_Orders = profile.total_orders
    Total_Clicks = 0
    Total_rateing = 0

    for r in presets: Total_Clicks += r.clicks
    for r in presets: Total_rateing += r.rateing
    

    context = {
        'orders': Total_Orders,
        'clicks': Total_Clicks,
        'rateing': Total_rateing,
    }

    return render(request, 'profiles/stats.html', context)


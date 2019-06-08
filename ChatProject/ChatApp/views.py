from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import jwt,json
from .forms import SignupForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):        # view for index
    return render(request, 'ChatApp/Index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):      # view for logout
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):       # view for login and and after login token generation
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                payload = {
                    'id': user.id,
                    'email': user.email,
                }
                jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
                print("11111111111111", jwt_token)
                login(request, user)
                return redirect('ChatApp:chatIndex')
                decode_jwt_token
            else:
                return HttpResponse("Your account was inactive.")

        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'ChatApp/login.html', {})


def signup(request):       # view for signup and email verification by sending activation link on users email
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('ChatApp/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            print("llllllllll", email)
            email.send()
            # return redirect('ChatApp/account_activation_sent')
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'ChatApp/signup.html', {'form': form})


def activate(request, uidb64, token):       #
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def chatindex(request):   # view of index page of chat app
    return render(request, 'ChatApp/chatIndex.html', {})


def room(request, room_name):   # view of chat room
    return render(request, 'ChatApp/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def email(request):     # view to sent email
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com',]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('redirect to a new page')

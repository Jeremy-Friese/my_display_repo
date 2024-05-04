import smtplib
import json
from decimal import Decimal
from datetime import datetime
import pytz

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView

import stripe

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#from .enc import secret

from main.models import Payment


stripe.api_key = settings.STRIPE_SECRET_KEY


def my_view(request):
    request.user_agent.is_mobile
    request.user_agent.is_tablet
    request.user_agent.is_touch_capable
    request.user_agent.is_pc
    request.user_agent.is_bot
    request.user_agent.browser
    request.user_agent.browser.family
    request.user_agent.browser.version
    request.user_agent.browser.version_string
    request.user_agent.os
    request.user_agent.os.family
    request.user_agent.os.version
    request.user_agent.os.version_string
    request.user_agent.device
    request.user_agent.device.family


def home(request):
    if request.method == "GET":
        response = render(request, "main.html", {})
        response["Server"] = "Four Seasons Server"
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-Frame-Options:"] = "SAMEORIGIN"
        return(response)
    elif request.method == "POST":
        data = request.POST.copy()
        name = data['your_name']
        email = data['email']
        number = data['number']
        message = data['message']
        gmailer(name, email, number, message)
        response = render(request, "main.html", {})
        response["Server"] = "Four Seasons Server"
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-Frame-Options:"] = "SAMEORIGIN"
        return(response)

def robots(request):
    response = render(request, "robots.txt")
    return(response)

# @csrf_exempt
# def payment(request):
#     if request.method == "GET":
#         response = render(request, "paymentII.html", {})
#         response["Server"] = "Four Seasons Server"
#         response["X-XSS-Protection"] = "1; mode=block"
#         response["X-Frame-Options:"] = "SAMEORIGIN"
#         return(response)
#     elif request.method == "POST":
#         data = request.POST.copy()
#         name = data["name"]
#         description = data["invoice"]
#         amount = data["amount"]
#         ccNumber = data["number"]
#         date = str(data["cc_exp"])
#         month = date[:2]
#         year = "20" + str(date[-2:])
#         ccv = data["id"]
#         cCard = getToken(ccNumber, month, year, ccv)
#         print(cCard["id"])
#         try:
#             charge = stripe.Charge.create(
#                 object=name,
#                 amount= int(amount) * 100,
#                 currency='usd',
#                 description=description,
#                 source=cCard["id"]
#             )
#             #print(charge)
#         except stripe.error.InvalidRequestError as err:
#             cCard = getToken(ccNumber, month, year, ccv)
#             stripe.Customer.create(
#               description=name,
#             )
#             cCard = getToken(ccNumber, month, year, ccv)
#             charge = stripe.Charge.create(
#                 amount= int(amount) * 100,
#                 currency='usd',
#                 description=description,
#                 source=cCard["id"]
#             )
#             #print(charge)
#         response = render(request, "thankyou.html", {})
#         response["Server"] = "Four Seasons Server"
#         response["X-XSS-Protection"] = "1; mode=block"
#         response["X-Frame-Options:"] = "SAMEORIGIN"
#         return(response)


class PaymentView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name="paymentII.html",
            context={"key": settings.STRIPE_PUBLISHABLE_KEY},
        )

    def post(self, request, *args, **kwargs):
        token_result = json.loads(request.POST["stripe_result"])

        if token_result.get("error"):
            return render(
                request=request,
                template_name="paymentII.html",
                context={
                    "key": settings.STRIPE_PUBLISHABLE_KEY,
                    "error": token_result.get("error")["message"]
                }
            )
        amount = Decimal(request.POST["amount"])
        try:
            charge_response = stripe.Charge.create(
                amount=int(amount * 100),
                currency='usd',
                metadata={
                    "cardholder_name": request.POST.get("cardholder_name", "NA")[:500],
                    "address": request.POST.get("address", "NA")[:500],
                    "email": request.POST.get("email", "NA")[:500],
                },
                receipt_email=request.POST.get("email", "NA")[:500],
                source=token_result["token"]["id"],
            )
            charge_response = json.loads(str(charge_response))
            Payment.objects.create(
                name=request.POST.get("cardholder_name", "NA"),
                email=request.POST.get("email", "NA"),
                address=request.POST.get("address", "NA"),
                amount=amount,
                stripe_charge_id=charge_response["id"],
                created_at=datetime.fromtimestamp(charge_response["created"], tz=pytz.utc)
            )
            return redirect(to="main:thankyou")
        except stripe.error.CardError as e:
            return render(
                request=request,
                template_name="paymentII.html",
                context={
                    "key": settings.STRIPE_PUBLISHABLE_KEY,
                    "error": e.error.message
                }
            )
        except Exception as e:
            print(e)
            return render(
                request=request,
                template_name="paymentII.html",
                context={
                    "key": settings.STRIPE_PUBLISHABLE_KEY,
                    "error": "Failed to process payment! Please try again."
                }
            )


def getToken(ccNumber, month, year, ccv):
    cCard = stripe.Token.create(
      card={
        "number": ccNumber,
        "exp_month": int(month),
        "exp_year": int(year),
        "cvc": ccv,
      },
    )
    return(cCard)

def about(request):
    if request.method == "GET":
        response = render(request, "about.html", {})
        response["Server"] = "Four Seasons Server"
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-Frame-Options:"] = "SAMEORIGIN"
        return(response)
    elif request.method == "POST":
        data = request.POST.copy()
        name = data['your_name']
        email = data['email']
        number = data['number']
        message = data['message']
        gmailer(name, email, number, message)
        response = render(request, "about.html", {})
        response["Server"] = "Four Seasons Server"
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-Frame-Options:"] = "SAMEORIGIN"
        return(response)

def services(request):
    if request.method == "GET":
        response = render(request, "services.html", {})
        response["Server"] = "Four Seasons Server"
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-Frame-Options:"] = "SAMEORIGIN"
        return(response)
    elif request.method == "POST":
        data = request.POST.copy()
        name = data['your_name']
        email = data['email']
        number = data['number']
        message = data['message']
        gmailer(name, email, number, message)
        response = render(request, "services.html", {})
        response["Server"] = "Four Seasons Server"
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-Frame-Options:"] = "SAMEORIGIN"
        return(response)

def sitemap(request):
    response = render(request, "sitemap.xml", {})
    response["Server"] = "Four Seasons Server"
    response["X-XSS-Protection"] = "1; mode=block"
    response["X-Frame-Options:"] = "SAMEORIGIN"
    return(response)

def terms(request):
    response = render(request, "terms.html", {})
    response["Server"] = "Four Seasons Server"
    response["X-XSS-Protection"] = "1; mode=block"
    response["X-Frame-Options:"] = "SAMEORIGIN"
    return(response)

def privacy(request):
    response = render(request, "privacy.html", {})
    response["Server"] = "Four Seasons Server"
    response["X-XSS-Protection"] = "1; mode=block"
    response["X-Frame-Options:"] = "SAMEORIGIN"
    return(response)



def thankyou(request):
    response = render(request, "thankyou.html", {})
    response["Server"] = "Four Seasons Server"
    response["X-XSS-Protection"] = "1; mode=block"
    response["X-Frame-Options:"] = "SAMEORIGIN"
    return(response)

def gmailer(name, email, number, message):
    clientSend(name, email, number, message)
    creds = secret.decrypt("u")
    creds = creds.split(",")
    uname = creds[0]
    p = creds[1]
    to = str(email)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Thank You For Contacting Four Seasons Lawn Care"
    msg['From'] = uname
    msg['To'] = to
    body = f"""
      <div style="text-align: center; height: 250%">
                <h1 style="color:green;">Thank you {name} for contacting Four Seasons Lawn Care.</h1>
                <p>Expect a call from our Lawn Professional, or office staff soon.</p><br><br>
      <img src="https://i.ibb.co/jrDYr92/emial-Flyer.jpg" alt="emial-Flyer" border="0" style="height: auto; width: 75%;" /></a>
      </div>

    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>"""
    message = MIMEText(body, "html")
    msg.attach(message)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(uname, p)
    server.sendmail(uname, to, msg.as_string())
    server.quit()

def clientSend(name, email, number, message):
    creds = secret.decrypt("u")
    creds = creds.split(",")
    uname = creds[0]
    p = creds[1]
    to = "mwhite@fourseasonslaws.com"
    #to = "jeremy@thefriese.com"
    subject  = "New Customer Contact Recieved"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = uname
    msg['To'] = to
    body = f"""
      <div style="text-align: center; height: 250%">
               <h1 style="color:green;">New Customer Contact Recieved.</h1>
               <center>
                <table border="1" cellpadding="10">
                  <th>Name</th>
                  <th>Number</th>
                  <th>Email</th>
                  <th>Message</th>
                <tr>
                  <td>{name}</td>
                  <td>{number}</td>
                  <td>{email}</td>
                  <td>{message}</td>
                </tr>
    </div>
    """
    message = MIMEText(body, "html")
    msg.attach(message)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(uname, p)
    server.sendmail(uname, to, msg.as_string())
    server.quit()

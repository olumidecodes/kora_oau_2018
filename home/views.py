from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from home import forms, models
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import random, string
from django.conf import settings
import json
from django.core import serializers
from home import forms

BankCodes = {
    'Access':'044',
    'Wema': '035A',
    'Diamond': '063',
    'Fidelity': '070',
    'FCMB': '214',
    'Sterling':'232',
    'Zenith': '057'


}
def index(request):
    user_details = models.User_Dashboard_Details.objects.get(user=request.user)
    args = {'user_details':user_details}
    return render(request, 'home/dashboard.html', args)


def getObject(request, id):
    obj = models.Ajo_Group_Details.objects.get(pk=id)
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data)




def ReceivePayment(request):
    if request.method == "GET":
        form = forms.ReceivePaymentForm
        args = {'form': form}
        return render(request, 'home/receivePaymentTemplate.html', args)
    if request.method == 'POST':
        account_name = request.POST['recipient_name']
        account_number = request.POST['account_number']
        bank_code = BankCodes[request.POST['bank']]
        description = request.POST['description']
        import requests, json

        headers = {
            'Authorization': 'Bearer sk_live_62e1ef19e3cc49e5f80ccc70b13d188ef6e6c79b',
            'Content-Type': 'application/json',
        }

        data = '{ \n   "type": "nuban",' \
               '\n   "name": "'+ account_name +'",' \
               '\n   "description": "'+ description +'",' \
               '\n   "account_number": "'+ account_number +'",' \
               '\n   "bank_code": "'+ bank_code +'",' \
               '\n   "currency": "NGN",' \
               '\n   "metadata": {' \
               '\n      "job": "Flesh Eater"' \
               '\n    }' \
               '\n }'

        response = requests.post('https://api.paystack.co/transferrecipient', headers=headers, data=data)
        json_data = json.loads(response.text)
        print(json_data)
        print(json_data['data']['recipient_code'])

        data = '{"source": "balance", "reason": "Calm down", "amount":100, "recipient":"' + json_data['data']['recipient_code'] + '"}'
        print(data)
        response = requests.post('https://api.paystack.co/transfer', headers=headers, data=data)
        json_response = json.loads(response)

        if json_response['status']:
            return HttpResponse("SUCCESSFUL")
        else:
            return HttpResponse("FAILED")


def RegistrationView(request):
    if request.method == "GET":
        form = forms.RegistrationForm
        args = {'form': form}

        return render(request, 'home/register.html', args)

    elif request.method == "POST":
        form = forms.RegistrationForm(request.POST)


        if form.is_valid:
            saved = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            saved.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

        return render(request, 'home/register.html', {'form':forms.RegistrationForm})


def LoginView(request):
    if request.method == "GET":
        return render(request, 'home/loginPage.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')



def createAjoGroup(request):
    ajo_code = ''
    def generate_Ajo_code():
        global ajo_code
        for number in range(2):
            ajo_code += random.choice(string.ascii_letters)
        for number in range(2):
            ajo_code += random.choice(string.digits)
        return ajo_code
    while True:
        try:
           models.Ajo_Group_Details.objects.get(ajo_code=ajo_code)
           break
        except:
            generate_Ajo_code()
    ajo_group = models.Ajo_Group_Details.objects.create()
    ajo_group.ajo_code = ajo_code
    ajo_group.contributors.add(request.user)
    user_details = models.User_Dashboard_Details.objects.get(user=request.user)
    user_details.ajo_groups.add(ajo_group)



def join_Ajo_Group(request, ajo_code):
    user_details = models.User_Dashboard_Details.objects.get(user=request.user)
    ajo_group = models.Ajo_Group_Details.objects.get(ajo_code=ajo_code)
    if request.user not in ajo_group.contributors.all():
        ajo_group.contributors.add(request.user)
        user_details.ajo_groups.add(ajo_group)



def PayToGroup(request, ajo_code, username):
    user = User.objects.get(username=username)
    ajo_group = models.Ajo_Group_Details.objects.get(ajo_code=ajo_code)
    money = ajo_group.money_to_be_contributed / ajo_group.contributors.count()
    reference_code = ''
    def generate_reference_code():
        global reference_code
        for number in range(2):
            reference_code += random.choice(string.digits)

        return reference_code
    while True:
        try:
           models.Transactions.objects.get(reference_code=reference_code)
           break
        except:
            generate_reference_code()
    args = {'money':money, 'email':user.email,
            'public_key':settings.PAYPAL_PUBLIC_KEY, 'reference_code':reference_code
            }
    if user not in ajo_group:
        return render(request, 'home/pay.html', args)
    else:
        return HttpResponse("You Have Paid Already")


def confirmTransactionStatus(reference_code):
    transaction = models.Transactions.objects.get(reference_code=reference_code)
    transaction.status = True
    transaction.save()
    return redirect('home')



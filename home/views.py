from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from home import forms, models
from django.contrib.auth import login, authenticate
import random, string
import json
from django.core import serializers
from home import forms

def index(request):
    user_details = models.User_Dashboard_Details.objects.get(user=request.user)
    args = {'user_details':user_details}
    return render(request, 'home/index.html', args)


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



def RegistrationView(request):
    if request.method == "GET":
        form = forms.RegistrationForm
        args = {'form': form}

        return render(request, 'home/registrationTemplate.html', args)

    elif request.method == "POST":
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            saved.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

        return render(request, 'home/registrationTemplate.html', {'form':forms.RegistrationForm})


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




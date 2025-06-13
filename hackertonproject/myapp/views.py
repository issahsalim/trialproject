import os
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
import json, requests   
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth import get_user_model


# Create your views here.


load_dotenv() 


User= get_user_model() 
# CHECKING EMAIL WHEN RESETTING PASSWORD 
class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = "email_reset_password.html"
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
          
            return super().form_valid(form)
        else:
           
            messages.error(self.request, "Email does not match any account")
            return self.form_invalid(form)
   


def index(request):
    return render(request,'index.html') 


# signup 
def registerView(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home')
        
    else:  
        form = userForm()
    return render(request, 'signup.html', {'form': form}) 


# login 
def loginView(request):
    if request.method=='POST':
        username=request.POST['username'] 
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:  
            messages.error(request,'Invalid username or password')
            return redirect('login')
    
    return render(request,'login.html') 


def logoutView(request):
    logout(request)
    return redirect('home') 

# ai chatbot 
def chatbot(request): 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            userinput = data.get('message') 
            
            payload = {
                "model": "deepseek/deepseek-r1-distill-llama-70b:free",
                "messages": [
                    {"role": "user", "content": userinput}
                ],
            } 

            headers = {
                "Authorization": f"Bearer {os.getenv('AI_API_KEY')}", 
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",   
                "X-Title": "My Chatbot"
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            result = response.json()

            ai_response = result["choices"][0]["message"]["content"] if "choices" in result else "No message received"  
                                 
            # ChatBot.objects.create(user=request.user, userinput=userinput, ai_response=ai_response)
            
            return JsonResponse({"ai_response": ai_response})

        except Exception as e:  
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)

    else:
        if request.user.is_authenticated:
            course = request.user.Course
            questionss=Questions.objects.all() 

            questions = [
                f"What is {course}?",
                f"Create five questions on {course}.",
                f"Who is the father of {course}?",
                f"Create a study plan for me on {course}.",
            ]

            fn = request.user.first_name[:1]
            ln = request.user.last_name[:1]
            
            return render(request, 'chatbot.html', {
                'questions': questions,
                'fn': fn,
                'ln': ln,
                'main':questionss
            })
        
        else:
            return render(request, 'chatbot.html', {'questions': []}) 


def search_place(request):
    query = request.GET.get('q', '')
    places = Place.objects.filter(name__icontains=query)
    data = [{
        'name': place.name,
        'lat': place.latitude,
        'lng': place.longitude,
        'image': place.image.url,
        'description': place.description
    } for place in places]
    return JsonResponse({'results': data})


def get_support_members(request):
    members = SupportMember.objects.all()
    data = [{
        'name': member.name,
        'photo': member.photo.url,
        'contact': member.contact_number
    } for member in members]
    return JsonResponse({'members': data})


def campusMap(request):
    return render(request,'map.html') 


def map_view(request):
    places = Place.objects.all().values('id', 'name', 'address', 'description', 'image', 'latitude', 'longitude', 'category')
    places_list = list(places)
    for place in places_list:
        place['image_url'] = request.build_absolute_uri(f'/media/{place["image"]}')
    return render(request, 'orginalmap.html', {'places': places_list})


def team_members_api(request):
    members = SupportMember.objects.all().values('name', 'contact_number', 'photo', 'role')
    members_list = list(members)
    for member in members_list:
        member['photo_url'] = request.build_absolute_uri(f'/media/{member["photo"]}')
    return JsonResponse(members_list, safe=False) 


# def campus_map(request):
#     places = Place.objects.all()
#     team_members = TeamMember.objects.all()
#     return render(request, 'orginalmap.html', {
#         'places': places,
#         'team_members': team_members,
#         'GOOGLE_MAPS_API_KEY': f'{os.getenv('GOOGLE_MAP_API')}',
#     })

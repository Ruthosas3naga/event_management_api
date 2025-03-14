from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Event Management API!, my endpoints are;"
    "https://osasenaga.pythonanywhere.com/api/events/", 
    "https://osasenaga.pythonanywhere.com/api/notiications/",
    "https://osasenaga.pythonanywhere.com/api/comments/")

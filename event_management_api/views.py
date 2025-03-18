from django.http import HttpResponse

def home(request):
    response_text = """
    Welcome to the Event Management API! My endpoints are:
    - <a href="https://osasenaga.pythonanywhere.com/api/login/">Login</a>
    - <a href="https://osasenaga.pythonanywhere.com/api/register/">Register</a>
    - <a href="https://osasenaga.pythonanywhere.com/api/events/">Events</a>
    - <a href="https://osasenaga.pythonanywhere.com/api/notifications/">Notifications</a>
    - <a href="https://osasenaga.pythonanywhere.com/api/comments/">Comments</a>
    """
    return HttpResponse(response_text, status=200) 

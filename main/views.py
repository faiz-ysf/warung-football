from django.shortcuts import render
from .models import News

def show_main(request):
    context = {
        'npm' : '240123456',
        'name': 'Haru Urara',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)


def news_list(request):
    articles = News.objects.all().order_by('-created_at')
    return render(request, "main.html", {"articles": articles})

# Create your views here.

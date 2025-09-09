from django.shortcuts import render
from .models import News

def show_main(request):
    context = {
        'npm' : '2406434292',
        'name': 'Faiz Yusuf Ridwan',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)


def news_list(request):
    articles = News.objects.all().order_by('-created_at')
    return render(request, "main.html", {"articles": articles})

# Create your views here.

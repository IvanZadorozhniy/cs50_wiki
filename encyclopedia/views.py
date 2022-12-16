from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    
    article = util.get_entry(title)
    if article:
        return render(request,"encyclopedia/article.html",{
            "title": title,
            "article": markdown2.markdown(article)
        })
    else:
        return HttpResponse(404)
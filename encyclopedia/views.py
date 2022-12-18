from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
from . import util
import random
import re
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


def search_request(request):
    query = request.GET['q'] if request.GET.get("q", False) else None
    if query:
        title = next((title for title in util.list_entries() if title.lower() == query.lower()), None)
        if title:    
            return redirect("title", title=title)
        else:
            pattern = re.compile(".*"+query)
            entries = [title for title in util.list_entries() if pattern.match(title.lower())]
            print(entries)
            if entries:
                return render(request, "encyclopedia/search.html", {
                    "entries": entries 
                })
            else: 
                return HttpResponse(404)
    else:
        return HttpResponse(404)


def create_article(request):
    if request.POST:
        title = request.POST['title']
        if title in util.list_entries():
            return HttpResponse("An article with that name already exists")
        
        article = request.POST['text_article']
        util.save_entry(title=title, content=article)
        
        return redirect("title", title=title)
    return render(request, "encyclopedia/create_article.html")

def random_article(request):
    return redirect("title", title=random.choice(util.list_entries()))

def edit_article(request, title):
    if request.POST:
        util.delete_entry(title=title)
        
        title = request.POST['title']
        if title in util.list_entries():
            return HttpResponse("An article with that name already exists")
        
        article = request.POST['text_article']
        util.save_entry(title=title, content=article)
        return redirect("title", title=title)
    content = util.get_entry(title)
    context = {
        "title": title,
        "text_article": content
    }
    return render(request, "encyclopedia/edit_article.html", context)
from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
from . import util

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
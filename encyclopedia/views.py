from django.shortcuts import render, redirect

from . import util

import markdown2

from django import forms

import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    content = util.get_entry(title)

    if content is not None:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
        "content": content,
        "heading": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": "<h1>Error: Page not found!</h1>",
            })

def search(request):
    if request.method == 'GET':
        list = util.list_entries()
        result = []
        title = request.GET.get("q")

        for item in list:

            if title.lower() in item.lower():
                result.append(item)

        if len(result) == 0:
            return render(request, "encyclopedia/entry.html", {
                "content": "<h1>Nothing Found! Please try again</h1>"
                })

        elif result[0] == title:
            return redirect("title", title=title)
 
        else:
            return render(request, "encyclopedia/result.html", {
                "result": result,
                "title":title
                })

def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")

    if request.method == 'POST':
        list = util.list_entries()

        title = request.POST.get("new_title")
        content = request.POST.get("new_entry")

        for item in list:
            if title.lower() in item.lower():
                return render(request, "encyclopedia/entry.html", {
                    "content": "<h2>Entry already exists!</h2>"
                    })

        util.save_entry(title, content)
        return redirect("new")

def edit(request):
    if request.method == 'GET':

        title = request.GET.get("title")
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
            })

    if request.method == 'POST':

        title = request.POST.get("edit_title")
        content = request.POST.get("new_content")

        util.save_entry(title, content)
        return redirect("title", title)

def rand(request):
    if request.method == 'GET':
        
        list = util.list_entries()
        list_len = len(list) - 1
        ran = random.randint(0, list_len)
        suggestion = list[ran]

        return redirect("title", title=suggestion)
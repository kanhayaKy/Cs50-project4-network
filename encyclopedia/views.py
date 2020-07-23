from django.shortcuts import render,redirect
from . import util
from django.http import HttpResponse,HttpResponseRedirect
from django import forms 
from . import util
from django.urls import reverse
import markdown2


class NewPage(forms.Form):
    title = forms.CharField(label = "Title")
    Contents = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def EntryPage(request , title):
    if title in util.list_entries():
        content = markdown2.markdown(f"{util.get_entry(title)}")
        return render(request,"encyclopedia/Entry.html",{
            "title":title,
            "content":content
        })
    else:
        return render(request,"encyclopedia/error.html") 


def CreatePage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["Contents"]
            if title in util.list_entries():
                 return render(request,"encyclopedia/error.html") 

            util.save_entry(title,content)

            return redirect("EntryPage",title)
        else:
            return render(request,"encyclopedia/create.html", { "form":form} )
    return render(request,"encyclopedia/create.html",{
        "form":NewPage()
    })


def EditPage(request, title=""):
    if request.method == 'POST':
        form = NewPage(request.POST)
        title = form['title']
        print(form.is_valid(),form.errors)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["Contents"]
            util.save_entry(title,content)
            return redirect("EntryPage",title)
        else:
            return render(request,"encyclopedia/edit.html", { "form":form} )


    form = NewPage(initial={'title':title,'Contents':util.get_entry(title)})
    return render(request,"encyclopedia/edit.html",{
        "form":form,
        "title":title
    })


def SearchPage(request):
    substr = request.POST["q"]
    entries = util.Filter(util.list_entries(),substr)
    print(substr,entries)
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "message":f"Search results for '{substr}'"
    })

def RandomPage(request):    
    title = util.random_entry()
    return redirect("EntryPage",title)
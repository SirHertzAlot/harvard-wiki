import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import Entry
from django.db.models import Q

from encyclopedia import util

class SearchForm(forms.Form):
    q = forms.CharField(label="Search")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

class EntryView(TemplateView):
    model = Entry
    template_name = 'encyclopedia/entry.html'

# Create your views here.
    
#Edit entry route
def edit_entry(request, title):
    if request.method == "POST":
        
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            # Isolate the entry from the 'cleaned' version of form data
            title = form.data["title"]
            content = form.data["content"]

            # Add the new entry to our list of entries
            util.save_entry(title, content)

            # Redirect user to list of entries
            return HttpResponseRedirect(reverse("index"))
    else:
        if request.session['entry'] == None:
            request.session['entry'] = title
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": util.get_entry(title),
            "entry_form": NewEntryForm(),
            "form": SearchForm()
        })

# Create Entry view with form to send markdown entry to backend for validation & processing. 
def index(request):
    return render(request, "encyclopedia/create.html", {
        #"placeholder": request.session['entry' or None],
        "entry_form": NewEntryForm(),
        "form": SearchForm()
    })

# Random Entry view to send markdown entry to client for viewing. 
def random_entry(request):
    if request.method == 'GET':
        entry_list = util.list_entries()
        entry = random.choice(entry_list)
        title = entry.splitlines(True)[0]
        return render(request,"encyclopedia/entry.html", {
            "entry": util.get_entry(entry),
            "title": title,
            "form": SearchForm(),
        })
    else:
        # Redirect user to list of entries
        return HttpResponseRedirect(reverse("index"))  

# Read Entry view to send markdown entry to client for viewing. 
def read_entry(request, title):

    if request.method == "GET":
        title = title.split("\r")[0]
        request.session['entry'] = title
        return render(request, "encyclopedia/read.html", {
            "entry": util.get_entry(title),
            "title":  title,
            "form": SearchForm()
        })
    else:
      # Redirect user to list of entries
        return HttpResponseRedirect(reverse("index"))  

# Create Entry form validation & processing. 
def submit_entry(request):
    
    form = NewEntryForm(request.POST)
    
    if request.method == 'POST':
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the entry from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Add the new entry to our list of entries
            util.save_entry(title, content)

            # Redirect user to list of entries
            return HttpResponseRedirect(reverse("index"))
    else:
        # If the form is invalid, re-render the page with existing information.
        return render(request, "encyclopedia/create.html", {
            "entry_form": form,
            "form": SearchForm()
        })
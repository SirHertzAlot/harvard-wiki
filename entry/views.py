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
    title = forms.CharField(label="title", required="true")
    content = forms.CharField(label="content", widget=forms.Textarea, required="true")

class EditEntryForm(forms.Form):
    title = forms.CharField(label="title", disabled="true")
    content = forms.CharField(widget=forms.Textarea, required="true")

class EntryView(TemplateView):
    model = Entry
    template_name = 'encyclopedia/entry.html'

# Create your views here.
    
#Edit entry route
def edit_entry(request, title):
    if request.method == "POST":
        
        form = EditEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            # Isolate the entry from the 'cleaned' version of form data
            title = form.data["title"]
            content = form.data["content"]

            # Add the new entry to our list of entries
            util.save_entry(title, content)

            # Redirect user to list of entries
            return HttpResponseRedirect(reverse(f"/wiki/{title}"))
    else:
        if request.session['entry'] == None:
            request.session['entry'] = title
        clean_title = title.splitlines(True)[0].split("#")[0].strip()
        entry = util.get_entry(clean_title)
        
        return render(request, "encyclopedia/edit.html", {
            "title": clean_title,
            "entry": util.get_entry(clean_title),
            "entry_form": EditEntryForm(initial={'content': entry, 'title': clean_title}),
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
        entry = util.get_entry(title)
        if entry is not None:
            return render(request, "encyclopedia/read.html", {
                "entry": util.get_entry(title),
                "title":  title,
                "form": SearchForm()
            })
        message = f"Entry for {title} does not exist. Please try a different entry A."
        return render(request, "encyclopedia/error.html", {
            "message": message,
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

            entries_list = util.list_entries()

            for entry in entries_list:
                processed_entry = entry.split()[0].lower()
                if title.lower() in processed_entry:
                    message = f"Entry for {title} already exists. Please try a different title."
                    return render(request, "encyclopedia/error.html", {
                        "message": message,
                        "form": SearchForm()
                    })

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
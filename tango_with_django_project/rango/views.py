from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page 


def index(request):
    #Query database for a list of ALL categories stored
    #order the categories by number of likes in descending order
    #retrieve only the top 5
    #Place the list in our context_dict dictionary(with our boldmessage!)
    #that will be passed to the template engine 
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]


    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list 
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request,'rango/about.html',)

def show_category(request, category_name_slug):
    #context dict which we pass to the template rendering engine
    context_dict = {}

    try:
        #can we find a categor name slug with the given name?
        #Ifnwe can't the .get() method raises a DoesNotExist exception
        #the .get() method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        #retrieve all of the associated pages 
        #filter() will return a list of page objects or emoty list
        pages = Page.objects.filter(category=category)

        #adds our results list to the template context under name pages
        context_dict['pages'] = pages 
        #also add the  category object from datatbase to the context dictionary
        #use this to verity that the category still exists 
        context_dict['category'] = category 
    except Category.DoesNotExist: 
        #answer we get if we didnt find the specified category 
        #dont do anything as the template will display the 'no category' for us 
        context_dict['category'] = None
        context_dict['pages'] = None 

    return render(request, 'rango/category.html', context=context_dict)
    
    

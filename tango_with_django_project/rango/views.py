from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page 
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse 


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

def add_category(request):
    form = CategoryForm()

    #HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #have we been provided with a valid form?
        if form.is_valid():
            #save the new category to the database.
            form.save(commit=True)
            #now that the category is saved, we could confirm this.
            #for now, just redirct the user back to the index view. 
            return redirect('/rango/')
        else:
            #the supplied form contained errors - 
            #just print them in the terminal 
            print(form.errors)

    #wil handle the bad form, new form, or no form supplied cases.
    #render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})
    
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category: 
                page = form.save(commit=False)
                page.category = category 
                page.views = 0 
                page.save()
                return redirect(reverse('rango:show_category', 
                                        kwargs={'category_name_slug':
                                                category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category' : category}
    return render(request, 'rango/add_page.html', context=context_dict)

            

